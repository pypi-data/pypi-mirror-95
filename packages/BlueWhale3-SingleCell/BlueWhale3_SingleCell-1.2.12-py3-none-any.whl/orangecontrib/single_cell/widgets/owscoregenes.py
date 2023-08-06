"""
Rank
====

Rank (score) features for prediction.

"""
import logging
import numpy as np

from collections import namedtuple, OrderedDict
from functools import partial
from itertools import chain
from scipy.sparse import issparse

from AnyQt.QtCore import Qt, QItemSelection, QItemSelectionRange, QItemSelectionModel
from AnyQt.QtGui import QFontMetrics
from AnyQt.QtWidgets import (
    QTableView,
    QRadioButton,
    QButtonGroup,
    QGridLayout,
    QStackedWidget,
    QHeaderView,
    QCheckBox,
    QItemDelegate,
)

from Orange.data import (
    Table,
    Domain,
    ContinuousVariable,
    DiscreteVariable,
    StringVariable,
    Variable,
)
from Orange.misc.cache import memoize_method
from Orange.preprocess import score
from Orange.widgets import report
from Orange.widgets import gui
from Orange.widgets.settings import DomainContextHandler, Setting, ContextSetting
from Orange.widgets.utils.itemmodels import PyTableModel
from Orange.widgets.utils.sql import check_sql_input
from Orange.widgets.widget import OWWidget, Msg, Input, Output

from orangecontrib.bioinformatics.widgets.utils.data import (
    TAX_ID,
    GENE_AS_ATTRIBUTE_NAME,
    GENE_ID_COLUMN,
    GENE_ID_ATTRIBUTE,
)

from orangecontrib.single_cell.i18n_config import *

log = logging.getLogger(__name__)


def __(key):
    return i18n.t('single_cell.owscoregenes.' + key)


class ProblemType:
    CLASSIFICATION, REGRESSION, UNSUPERVISED = range(3)

    @classmethod
    def from_variable(cls, variable):
        return (cls.CLASSIFICATION if isinstance(variable, DiscreteVariable) else
                cls.REGRESSION if isinstance(variable, ContinuousVariable) else
                cls.UNSUPERVISED)


class UnsupervisedScorer(score.Scorer):
    """
    Simple unsupervised scorer for datasets without target variable.
    """
    feature_type = Variable

    def __call__(self, data, feature=None):
        if feature is not None:
            f = data.domain[feature]
            data = data.transform(Domain([f], data.domain.class_vars))

        for pp in self.preprocessors:
            data = pp(data)

        for var in data.domain.attributes:
            if not isinstance(var, self.feature_type):
                raise ValueError(
                    "{} cannot score {} variables."
                        .format(self.friendly_name,
                                self._friendly_vartype_name(type(var))))

        return self.score_data(data, feature)


class MeanScorer(UnsupervisedScorer):
    """
    Simple scorer returning mean of the features.
    Return NA for non-continuos columns to enable mixtures of discrete and continuous variables.
    """
    supports_sparse_data = True
    friendly_name = "Mean"

    def score_data(self, data, feature):
        weights = np.nan + np.zeros((len(data.domain.attributes)))
        conts = np.array([a.is_continuous for a in data.domain.attributes])
        weights[conts] = data.X[:, conts].mean(axis=0)

        if feature:
            return weights[0]
        return weights


class VarianceScorer(UnsupervisedScorer):
    """
    Simple scorer returning variance of the features.
    """
    supports_sparse_data = False
    friendly_name = "Variance"

    def score_data(self, data, feature):
        weights = np.nan + np.zeros((len(data.domain.attributes)))
        conts = np.array([a.is_continuous for a in data.domain.attributes])
        weights[conts] = np.var(data.X[:, conts], axis=0)

        if feature:
            return weights[0]
        return weights


class DispersionScorer(UnsupervisedScorer):
    """
    Simple scorer returning approximate dispersion (variance / mean) of the features.
    """
    supports_sparse_data = False
    friendly_name = "Dispersion"

    def score_data(self, data, feature):
        weights = np.nan + np.zeros((len(data.domain.attributes)))
        conts = np.array([a.is_continuous for a in data.domain.attributes])

        means = data.X[:, conts].mean(axis=0)
        variances = np.var(data.X[:, conts], axis=0)
        means[means == 0] = 1
        weights[conts] = variances / means

        if feature:
            return weights[0]
        return weights


class VariationCoefficientScorer(UnsupervisedScorer):
    """
    Simple scorer returning coefficient of variation.
    http://www.statisticshowto.com/how-to-find-a-coefficient-of-variation/
    """
    supports_sparse_data = False
    friendly_name = "Coef. of Variation"

    def score_data(self, data, feature):
        weights = np.nan + np.zeros((len(data.domain.attributes)))
        conts = np.array([a.is_continuous for a in data.domain.attributes])

        means = data.X[:, conts].mean(axis=0)
        stds = data.X[:, conts].std(axis=0)
        means[means == 0] = 1
        weights[conts] = stds / means

        if feature:
            return weights[0]
        return weights


ScoreMeta = namedtuple("score_meta", ["name", "shortname", "scorer", 'problem_type', 'is_default'])

# Default scores.
CLS_SCORES = [
    ScoreMeta(__("btn.info_gain"), __("label.info_gain"), score.InfoGain, ProblemType.CLASSIFICATION, False),
]
REG_SCORES = [
    ScoreMeta(__("btn.univar_reg"), __("label.univar_reg"), score.UnivariateLinearRegression, ProblemType.REGRESSION,
              True),
]
UNSUP_SCORES = [
    ScoreMeta(__("btn.mean"), __("lable.mean"), MeanScorer, ProblemType.UNSUPERVISED, True),
    ScoreMeta(__("btn.variance"), __("lable.variance"), VarianceScorer, ProblemType.UNSUPERVISED, True),
    ScoreMeta(__("btn.dispersion"), __("lable.dispersion"), DispersionScorer, ProblemType.UNSUPERVISED, False),
    ScoreMeta(__("btn.cv"), __("lable.cv"), VariationCoefficientScorer, ProblemType.UNSUPERVISED, False),
]

SCORES = CLS_SCORES + UNSUP_SCORES


class TableView(QTableView):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent,
                         selectionBehavior=QTableView.SelectRows,
                         selectionMode=QTableView.ExtendedSelection,
                         sortingEnabled=True,
                         showGrid=True,
                         cornerButtonEnabled=False,
                         alternatingRowColors=False,
                         **kwargs)
        self.setItemDelegate(gui.ColoredBarItemDelegate(self))
        self.setItemDelegateForColumn(0, QItemDelegate())

        header = self.verticalHeader()
        header.setSectionResizeMode(header.Fixed)
        header.setFixedWidth(50)
        header.setDefaultSectionSize(22)
        header.setTextElideMode(Qt.ElideMiddle)  # Note: https://bugreports.qt.io/browse/QTBUG-62091

        header = self.horizontalHeader()
        header.setSectionResizeMode(header.Fixed)
        header.setFixedHeight(24)
        header.setDefaultSectionSize(80)
        header.setTextElideMode(Qt.ElideMiddle)

    def setVHeaderFixedWidthFromLabel(self, max_label):
        header = self.verticalHeader()
        width = QFontMetrics(header.font()).width(max_label)
        header.setFixedWidth(min(width + 40, 400))


class TableModel(PyTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extremes = {}

    def data(self, index, role=Qt.DisplayRole, _isnan=np.isnan):
        if role == gui.BarRatioRole and index.isValid():
            value = super().data(index, Qt.EditRole)
            if not isinstance(value, float):
                return None
            vmin, vmax = self._extremes.get(index.column(), (-np.inf, np.inf))
            value = (value - vmin) / ((vmax - vmin) or 1)
            return value

        if role == Qt.DisplayRole:
            role = Qt.EditRole

        value = super().data(index, role)

        # Display nothing for non-existent attr value counts in the first column
        if role == Qt.EditRole and index.column() == 0 and _isnan(value):
            return ''

        return value

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.InitialSortOrderRole:
            return Qt.DescendingOrder
        return super().headerData(section, orientation, role)

    def setExtremesFrom(self, column, values):
        """Set extremes for columnn's ratio bars from values"""
        try:
            vmin = np.nanmin(values)
            if np.isnan(vmin):
                raise TypeError
        except TypeError:
            vmin, vmax = -np.inf, np.inf
        else:
            vmax = np.nanmax(values)
        self._extremes[column] = (vmin, vmax)

    def resetSorting(self, yes_reset=False):
        """We don't want to invalidate our sort proxy model everytime we
        wrap a new list. Our proxymodel only invalidates explicitly
        (i.e. when new data is set)"""
        if yes_reset:
            super().resetSorting()

    def _argsortData(self, data, order):
        """Always sort NaNs last"""
        indices = np.argsort(data, kind='mergesort')
        if order == Qt.DescendingOrder:
            return np.roll(indices[::-1], -np.isnan(data).sum())
        return indices


class OWRank(OWWidget):
    name = __('name')
    description = __("desc")
    icon = "icons/ScoreGenes.svg"
    priority = 310

    buttons_area_orientation = Qt.Vertical

    class Inputs:
        data = Input('Data', Table, label=i18n.t("single_cell.common.data"))
        scorer = Input("Scorer", score.Scorer, multiple=True, label=i18n.t("single_cell.common.scorer"))

    class Outputs:
        reduced_data = Output("Reduced Data", Table, default=True, label=i18n.t("single_cell.common.reduced_data"))
        scores = Output("Scores", Table, label=i18n.t("single_cell.common.scores"))

    SelectNone, SelectAll, SelectManual, SelectNBest = range(4)

    nSelected = Setting(5)
    auto_apply = Setting(True)

    sorting = Setting((0, Qt.DescendingOrder))
    selected_methods = Setting(set())

    settings_version = 2
    settingsHandler = DomainContextHandler()
    selected_rows = ContextSetting([])
    selectionMethod = ContextSetting(SelectNBest)

    class Information(OWWidget.Information):
        no_target_var = Msg(__('msg.no_target_var'))
        missings_imputed = Msg(__('msg.missings_imputed'))

    class Error(OWWidget.Error):
        invalid_type = Msg(__('msg.invalid_type'))
        inadequate_learner = Msg(__('msg.inadequate_learner'))
        no_attributes = Msg(__('msg.no_attributes'))

    def __init__(self):
        super().__init__()
        self.scorers = OrderedDict()
        self.out_domain_desc = None
        self.data = None
        self.problem_type_mode = ProblemType.CLASSIFICATION

        # input data attributes
        self.tax_id = None
        self.use_attr_names = None
        self.gene_id_attribute = None
        self.gene_id_column = None

        if not self.selected_methods:
            self.selected_methods = {method.name for method in SCORES
                                     if method.is_default}

        # GUI

        self.ranksModel = model = TableModel(parent=self)  # type: TableModel
        self.ranksView = view = TableView(self)  # type: TableView
        self.mainArea.layout().addWidget(view)
        view.setModel(model)
        view.setColumnWidth(0, 30)
        view.selectionModel().selectionChanged.connect(self.on_select)

        def _set_select_manual():
            self.setSelectionMethod(OWRank.SelectManual)

        view.pressed.connect(_set_select_manual)
        view.verticalHeader().sectionClicked.connect(_set_select_manual)
        view.horizontalHeader().sectionClicked.connect(self.headerClick)

        self.measuresStack = stacked = QStackedWidget(self)
        self.controlArea.layout().addWidget(stacked)

        # Allow unsupervised scorers for any problem type
        for scoring_methods in (CLS_SCORES + UNSUP_SCORES,
                                REG_SCORES + UNSUP_SCORES,
                                UNSUP_SCORES,
                                []):
            box = gui.vBox(None, __('box.scoring_methods') if scoring_methods else None)
            stacked.addWidget(box)
            for method in scoring_methods:
                box.layout().addWidget(QCheckBox(
                    method.name, self,
                    objectName=method.shortname,  # To be easily found in tests
                    checked=method.name in self.selected_methods,
                    stateChanged=partial(self.methodSelectionChanged, method_name=method.name)))
            gui.rubber(box)

        gui.rubber(self.controlArea)
        self.switchProblemType(ProblemType.CLASSIFICATION)

        selMethBox = gui.vBox(self.controlArea, __('box.select_genes'), addSpace=True)

        grid = QGridLayout()
        grid.setContentsMargins(6, 0, 6, 0)
        self.selectButtons = QButtonGroup()
        self.selectButtons.buttonClicked[int].connect(self.setSelectionMethod)

        def button(text, buttonid, toolTip=None):
            b = QRadioButton(text)
            self.selectButtons.addButton(b, buttonid)
            if toolTip is not None:
                b.setToolTip(toolTip)
            return b

        b1 = button(self.tr(__('btn.none')), OWRank.SelectNone)
        b2 = button(self.tr(__("btn.all")), OWRank.SelectAll)
        b3 = button(self.tr(__("btn.manual")), OWRank.SelectManual)
        b4 = button(self.tr(__('btn.best_ranked')), OWRank.SelectNBest)

        s = gui.spin(selMethBox, self, "nSelected", 1, 1000,
                     callback=lambda: self.setSelectionMethod(OWRank.SelectNBest))

        grid.addWidget(b1, 0, 0)
        grid.addWidget(b2, 1, 0)
        grid.addWidget(b3, 2, 0)
        grid.addWidget(b4, 3, 0)
        grid.addWidget(s, 3, 1)

        self.selectButtons.button(self.selectionMethod).setChecked(True)

        selMethBox.layout().addLayout(grid)

        gui.auto_commit(selMethBox, self, "auto_apply", __("btn.send"), box=False)

        self.resize(690, 500)

    def switchProblemType(self, index):
        """
        Switch between discrete/continuous/no_class mode
        """
        self.measuresStack.setCurrentIndex(index)
        self.problem_type_mode = index

    @Inputs.data
    @check_sql_input
    def setData(self, data):
        self.closeContext()
        self.selected_rows = []
        self.ranksModel.clear()
        self.ranksModel.resetSorting(True)

        self.get_method_scores.cache_clear()
        self.get_scorer_scores.cache_clear()

        self.Error.clear()
        self.Information.clear()
        self.Information.missings_imputed(
            shown=data is not None and data.has_missing())

        if data is not None and not len(data.domain.attributes):
            self.Error.no_attributes()
            data = None

        self.data = data
        self.switchProblemType(ProblemType.CLASSIFICATION)
        if self.data is not None:
            self.tax_id = str(self.data.attributes.get(TAX_ID, None))
            self.use_attr_names = self.data.attributes.get(GENE_AS_ATTRIBUTE_NAME, None)
            self.gene_id_attribute = self.data.attributes.get(GENE_ID_ATTRIBUTE, None)
            self.gene_id_column = self.data.attributes.get(GENE_ID_COLUMN, None)
            domain = self.data.domain

            if domain.has_discrete_class:
                problem_type = ProblemType.CLASSIFICATION
            elif domain.has_continuous_class:
                problem_type = ProblemType.REGRESSION
            elif not domain.class_var:
                # self.Information.no_target_var()
                problem_type = ProblemType.UNSUPERVISED
            else:
                # This can happen?
                self.Error.invalid_type(type(domain.class_var).__name__)
                problem_type = None

            if problem_type is not None:
                self.switchProblemType(problem_type)

            self.ranksModel.setVerticalHeaderLabels(domain.attributes)
            self.ranksView.setVHeaderFixedWidthFromLabel(
                max((a.name for a in domain.attributes), key=len))

            self.selectionMethod = OWRank.SelectNBest

        self.openContext(data)

    def handleNewSignals(self):
        self.setStatusMessage(__('status.running'))
        self.updateScores()
        self.setStatusMessage('')
        self.on_select()

    @Inputs.scorer
    def set_learner(self, scorer, id):
        if scorer is None:
            self.scorers.pop(id, None)
        else:
            # Avoid caching a (possibly stale) previous instance of the same
            # Scorer passed via the same signal
            if id in self.scorers:
                self.get_scorer_scores.cache_clear()

            self.scorers[id] = ScoreMeta(scorer.name, scorer.name, scorer,
                                         ProblemType.from_variable(scorer.class_type),
                                         False)

    @memoize_method()
    def get_method_scores(self, method):
        estimator = method.scorer()
        data = self.data
        try:
            scores = np.asarray(estimator(data))
        except ValueError:
            log.warning("Scorer %s wasn't able to compute all scores at once",
                        method.name)
            try:
                scores = np.array([estimator(data, attr)
                                   for attr in data.domain.attributes])
            except ValueError:
                log.error(
                    "Scorer %s wasn't able to compute scores at all",
                    method.name)
                scores = np.full(len(data.domain.attributes), np.nan)
        return scores

    @memoize_method()
    def get_scorer_scores(self, scorer):
        try:
            scores = scorer.scorer.score_data(self.data).T
        except ValueError:
            log.error(
                "Scorer %s wasn't able to compute scores at all",
                scorer.name)
            scores = np.full((len(self.data.domain.attributes), 1), np.nan)

        labels = ((scorer.shortname,)
                  if scores.shape[1] == 1 else
                  tuple(scorer.shortname + '_' + str(i)
                        for i in range(1, 1 + scores.shape[1])))
        return scores, labels

    def updateScores(self):
        if self.data is None:
            self.ranksModel.clear()
            self.Outputs.scores.send(None)
            return

        methods = [method
                   for method in SCORES
                   if (method.name in self.selected_methods and
                       (method.problem_type == self.problem_type_mode or
                        method.problem_type == ProblemType.UNSUPERVISED) and
                       (not issparse(self.data.X) or
                        method.scorer.supports_sparse_data))]

        scorers = []
        self.Error.inadequate_learner.clear()
        for scorer in self.scorers.values():
            if scorer.problem_type in (self.problem_type_mode, ProblemType.UNSUPERVISED):
                scorers.append(scorer)
            else:
                self.Error.inadequate_learner(scorer.name, scorer.learner_adequacy_err_msg)

        method_scores = tuple(self.get_method_scores(method)
                              for method in methods)

        scorer_scores, scorer_labels = (), ()
        if scorers:
            scorer_scores, scorer_labels = zip(*(self.get_scorer_scores(scorer)
                                                 for scorer in scorers))
            scorer_labels = tuple(chain.from_iterable(scorer_labels))

        labels = tuple(method.shortname for method in methods) + scorer_labels
        model_array = np.column_stack(
            ([len(a.values) if a.is_discrete else np.nan
              for a in self.data.domain.attributes],) +
            (method_scores if method_scores else ()) +
            (scorer_scores if scorer_scores else ())
        )
        for column, values in enumerate(model_array.T):
            self.ranksModel.setExtremesFrom(column, values)

        self.ranksModel.wrap(model_array.tolist())
        self.ranksModel.setHorizontalHeaderLabels(('#',) + labels)
        self.ranksView.setColumnWidth(0, 40)

        # Re-apply sort
        try:
            sort_column, sort_order = self.sorting
            if sort_column < len(labels):
                self.ranksModel.sort(sort_column + 1, sort_order)  # +1 for '#' (discrete count) column
                self.ranksView.horizontalHeader().setSortIndicator(sort_column + 1, sort_order)
        except ValueError:
            pass

        self.autoSelection()
        self.Outputs.scores.send(self.create_scores_table(labels))

    def on_select(self):
        # Save indices of attributes in the original, unsorted domain
        self.selected_rows = self.ranksModel.mapToSourceRows([
            i.row() for i in self.ranksView.selectionModel().selectedRows(0)])
        self.commit()

    def setSelectionMethod(self, method):
        if self.selectionMethod != method:
            self.selectionMethod = method
            self.selectButtons.button(method).setChecked(True)
        self.autoSelection()
        self.on_select()

    def autoSelection(self):
        selModel = self.ranksView.selectionModel()
        model = self.ranksModel
        rowCount = model.rowCount()
        columnCount = model.columnCount()

        if self.selectionMethod == OWRank.SelectNone:
            selection = QItemSelection()
        elif self.selectionMethod == OWRank.SelectAll:
            selection = QItemSelection(
                model.index(0, 0),
                model.index(rowCount - 1, columnCount - 1)
            )
        elif self.selectionMethod == OWRank.SelectNBest:
            nSelected = min(self.nSelected, rowCount)
            selection = QItemSelection(
                model.index(0, 0),
                model.index(nSelected - 1, columnCount - 1)
            )
        else:
            selection = QItemSelection()
            if len(self.selected_rows):
                for row in model.mapFromSourceRows(self.selected_rows):
                    selection.append(QItemSelectionRange(
                        model.index(row, 0), model.index(row, columnCount - 1)))

        selModel.select(selection, QItemSelectionModel.ClearAndSelect)

    def headerClick(self, index):
        if index >= 1 and self.selectionMethod == OWRank.SelectNBest:
            # Reselect the top ranked attributes
            self.autoSelection()

        # Store the header states
        sort_order = self.ranksModel.sortOrder()
        sort_column = self.ranksModel.sortColumn() - 1  # -1 for '#' (discrete count) column
        self.sorting = (sort_column, sort_order)

    def methodSelectionChanged(self, state, method_name):
        if state == Qt.Checked:
            self.selected_methods.add(method_name)
        elif method_name in self.selected_methods:
            self.selected_methods.remove(method_name)

        self.updateScores()

    def send_report(self):
        if not self.data:
            return
        self.report_domain(__("report.input"), self.data.domain)
        self.report_table(__("report.ranks"), self.ranksView, num_format="{:.3f}")
        if self.out_domain_desc is not None:
            self.report_items(__("report.output"), self.out_domain_desc)

    def commit(self):
        selected_attrs = []
        if self.data is not None:
            attributes = self.data.domain.attributes
            selected_attrs = [attributes[i] for i in self.selected_rows]
        if not selected_attrs:
            self.Outputs.reduced_data.send(None)
            self.out_domain_desc = None
        else:
            reduced_domain = Domain(
                selected_attrs, self.data.domain.class_var, self.data.domain.metas)
            data = self.data.transform(reduced_domain)
            self.Outputs.reduced_data.send(data)
            self.out_domain_desc = report.describe_domain(data.domain)

    def create_scores_table(self, labels):

        model_list = self.ranksModel.tolist()
        if not model_list or len(model_list[0]) == 1:  # Empty or just n_values column
            return None

        feature_var = StringVariable("Feature")
        feature_id_var = StringVariable(self.gene_id_attribute if self.gene_id_attribute else 'Feature ID')

        domain = Domain([ContinuousVariable(label) for label in labels], metas=[feature_var, feature_id_var])
        features = np.array([[col.name, col.attributes.get(self.gene_id_attribute, '?')]
                             for col in self.data.domain.attributes])

        # Prevent np.inf scores
        finfo = np.finfo(np.float64)
        scores = np.clip(np.array(model_list)[:, 1:], finfo.min, finfo.max)

        new_table = Table(domain, scores, metas=features)
        new_table.attributes[TAX_ID] = self.tax_id
        new_table.attributes[GENE_AS_ATTRIBUTE_NAME] = False
        new_table.attributes[GENE_ID_COLUMN] = feature_id_var.name
        new_table.name = "Feature Scores"
        return new_table

    @classmethod
    def migrate_settings(cls, settings, version):
        # If older settings, restore sort header to default
        # Saved selected_rows will likely be incorrect
        if version is None or version < 2:
            column, order = 0, Qt.DescendingOrder
            headerState = settings.pop("headerState", None)

            # Lacking knowledge of last problemType, use discrete ranks view's ordering
            if isinstance(headerState, (tuple, list)):
                headerState = headerState[0]

            if isinstance(headerState, bytes):
                hview = QHeaderView(Qt.Horizontal)
                hview.restoreState(headerState)
                column, order = hview.sortIndicatorSection() - 1, hview.sortIndicatorOrder()
            settings["sorting"] = (column, order)

    @classmethod
    def migrate_context(cls, context, version):
        if version is None or version < 2:
            # Old selection was saved as sorted indices. New selection is original indices.
            # Since we can't devise the latter without first computing the ranks,
            # just reset the selection to avoid confusion.
            context.values['selected_rows'] = []


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    from Orange.classification import RandomForestLearner

    a = QApplication([])
    ow = OWRank()
    ow.set_learner(RandomForestLearner(), (3, 'Learner', None))
    ow.setData(Table("heart_disease.tab"))
    ow.show()
    a.exec_()
    ow.saveSettings()
