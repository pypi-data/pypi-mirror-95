import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import isEqual from 'lodash/isEqual';
import AreaChart from 'app/components/charts/areaChart';
import LineChart from 'app/components/charts/lineChart';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import { getSeriesSelection } from 'app/components/charts/utils';
import { parseStatsPeriod } from 'app/components/organizations/timeRangeSelector/utils';
import QuestionTooltip from 'app/components/questionTooltip';
import { defined } from 'app/utils';
import { getUtcDateString } from 'app/utils/dates';
import { axisDuration } from 'app/utils/discover/charts';
import { getExactDuration } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { getSessionTermDescription, SessionTerm, sessionTerm, } from '../../../utils/sessionTerm';
import { YAxis } from './releaseChartControls';
var HealthChart = /** @class */ (function (_super) {
    __extends(HealthChart, _super);
    function HealthChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { unselectedSeries: Object.keys(selected).filter(function (key) { return !selected[key]; }) }) });
            browserHistory.replace(to);
        };
        _this.formatTooltipValue = function (value) {
            var yAxis = _this.props.yAxis;
            switch (yAxis) {
                case YAxis.SESSION_DURATION:
                    return typeof value === 'number' ? getExactDuration(value, true) : '\u2015';
                case YAxis.CRASH_FREE:
                    return defined(value) ? value + "%" : '\u2015';
                case YAxis.SESSIONS:
                case YAxis.USERS:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        return _this;
    }
    HealthChart.prototype.componentDidMount = function () {
        if (this.shouldUnselectHealthySeries()) {
            this.props.onVisibleSeriesRecalculated();
            this.handleLegendSelectChanged({ selected: { Healthy: false } });
        }
    };
    HealthChart.prototype.shouldComponentUpdate = function (nextProps) {
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (this.props.location.query.unselectedSeries !==
            nextProps.location.query.unselectedSeries) {
            return true;
        }
        if (isEqual(this.props.timeseriesData, nextProps.timeseriesData)) {
            return false;
        }
        return true;
    };
    HealthChart.prototype.shouldUnselectHealthySeries = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, location = _a.location, shouldRecalculateVisibleSeries = _a.shouldRecalculateVisibleSeries;
        var otherAreasThanHealthyArePositive = timeseriesData
            .filter(function (s) { return s.seriesName !== sessionTerm.healthy; })
            .some(function (s) { return s.data.some(function (d) { return d.value > 0; }); });
        var alreadySomethingUnselected = !!decodeScalar(location.query.unselectedSeries);
        return (shouldRecalculateVisibleSeries &&
            otherAreasThanHealthyArePositive &&
            !alreadySomethingUnselected);
    };
    HealthChart.prototype.configureYAxis = function () {
        var yAxis = this.props.yAxis;
        switch (yAxis) {
            case YAxis.CRASH_FREE:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: '{value}%',
                        color: theme.chartLabel,
                    },
                };
            case YAxis.SESSION_DURATION:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return axisDuration(value * 1000); },
                        color: theme.chartLabel,
                    },
                };
            case YAxis.SESSIONS:
            case YAxis.USERS:
            default:
                return undefined;
        }
    };
    HealthChart.prototype.configureXAxis = function () {
        var _a = this.props, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps;
        if (timeseriesData.every(function (s) { return s.data.length === 1; })) {
            if (zoomRenderProps.period) {
                var _b = parseStatsPeriod(zoomRenderProps.period, null), start = _b.start, end = _b.end;
                return { min: start, max: end };
            }
            return {
                min: getUtcDateString(zoomRenderProps.start),
                max: getUtcDateString(zoomRenderProps.end),
            };
        }
        return undefined;
    };
    HealthChart.prototype.getChart = function () {
        var yAxis = this.props.yAxis;
        switch (yAxis) {
            case YAxis.SESSION_DURATION:
                return AreaChart;
            case YAxis.SESSIONS:
            case YAxis.USERS:
                return StackedAreaChart;
            case YAxis.CRASH_FREE:
            default:
                return LineChart;
        }
    };
    HealthChart.prototype.getLegendTooltipDescription = function (serieName) {
        var platform = this.props.platform;
        switch (serieName) {
            case sessionTerm.crashed:
                return getSessionTermDescription(SessionTerm.CRASHED, platform);
            case sessionTerm.abnormal:
                return getSessionTermDescription(SessionTerm.ABNORMAL, platform);
            case sessionTerm.errored:
                return getSessionTermDescription(SessionTerm.ERRORED, platform);
            case sessionTerm.healthy:
                return getSessionTermDescription(SessionTerm.HEALTHY, platform);
            case sessionTerm['crash-free-users']:
                return getSessionTermDescription(SessionTerm.CRASH_FREE_USERS, platform);
            case sessionTerm['crash-free-sessions']:
                return getSessionTermDescription(SessionTerm.CRASH_FREE_SESSIONS, platform);
            default:
                return '';
        }
    };
    HealthChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, timeseriesData = _a.timeseriesData, zoomRenderProps = _a.zoomRenderProps, location = _a.location, title = _a.title, help = _a.help;
        var Chart = this.getChart();
        var legend = {
            right: 10,
            top: 0,
            data: timeseriesData.map(function (d) { return d.seriesName; }).reverse(),
            selected: getSeriesSelection(location),
            tooltip: {
                show: true,
                // TODO(ts) tooltip.formatter has incorrect types in echarts 4
                formatter: function (params) {
                    var _a;
                    var seriesNameDesc = _this.getLegendTooltipDescription((_a = params.name) !== null && _a !== void 0 ? _a : '');
                    if (!seriesNameDesc) {
                        return '';
                    }
                    return ['<div class="tooltip-description">', seriesNameDesc, '</div>'].join('');
                },
            },
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {title}
          {help && <QuestionTooltip size="sm" position="top" title={help}/>}
        </HeaderTitleLegend>

        <Chart legend={legend} {...zoomRenderProps} series={timeseriesData} isGroupedByDate seriesOptions={{
            showSymbol: false,
        }} grid={{
            left: '10px',
            right: '10px',
            top: '40px',
            bottom: '0px',
        }} yAxis={this.configureYAxis()} xAxis={this.configureXAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>
      </React.Fragment>);
    };
    return HealthChart;
}(React.Component));
export default HealthChart;
//# sourceMappingURL=healthChart.jsx.map