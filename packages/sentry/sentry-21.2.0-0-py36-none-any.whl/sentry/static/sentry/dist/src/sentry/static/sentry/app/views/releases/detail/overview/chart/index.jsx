import { __assign, __extends } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import EventsChart from 'app/components/charts/eventsChart';
import { ChartContainer, HeaderTitleLegend } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import { decodeScalar } from 'app/utils/queryString';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
import HealthChartContainer from './healthChartContainer';
import ReleaseChartControls, { PERFORMANCE_AXIS, YAxis, } from './releaseChartControls';
import { getReleaseEventView } from './utils';
var ReleaseChartContainer = /** @class */ (function (_super) {
    __extends(ReleaseChartContainer, _super);
    function ReleaseChartContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The top events endpoint used to generate these series is not guaranteed to return a series
         * for both the current release and the other releases. This happens when there is insufficient
         * data. In these cases, the endpoint will return a single zerofilled series for the current
         * release.
         *
         * This is problematic as we want to show both series even if one is empty. To deal with this,
         * we clone the non empty series (to preserve the timestamps) with value 0 (to represent the
         * lack of data).
         */
        _this.seriesTransformer = function (series) {
            var current = null;
            var others = null;
            var allSeries = [];
            series.forEach(function (s) {
                if (s.seriesName === 'current' || s.seriesName === t('This Release')) {
                    current = s;
                }
                else if (s.seriesName === 'others' || s.seriesName === t('Other Releases')) {
                    others = s;
                }
                else {
                    allSeries.push(s);
                }
            });
            if (current !== null && others === null) {
                others = _this.cloneSeriesAsZero(current);
            }
            else if (current === null && others !== null) {
                current = _this.cloneSeriesAsZero(others);
            }
            if (others !== null) {
                others.seriesName = t('Other Releases');
                allSeries.unshift(others);
            }
            if (current !== null) {
                current.seriesName = t('This Release');
                allSeries.unshift(current);
            }
            return allSeries;
        };
        return _this;
    }
    ReleaseChartContainer.prototype.getTransactionsChartColors = function () {
        var _a = this.props, yAxis = _a.yAxis, theme = _a.theme;
        switch (yAxis) {
            case YAxis.FAILED_TRANSACTIONS:
                return [theme.red300, theme.red100];
            default:
                return [theme.purple300, theme.purple100];
        }
    };
    ReleaseChartContainer.prototype.getChartTitle = function () {
        var _a = this.props, yAxis = _a.yAxis, organization = _a.organization;
        switch (yAxis) {
            case YAxis.SESSIONS:
                return {
                    title: t('Session Count'),
                    help: t('The number of sessions in a given period.'),
                };
            case YAxis.USERS:
                return {
                    title: t('User Count'),
                    help: t('The number of users in a given period.'),
                };
            case YAxis.SESSION_DURATION:
                return { title: t('Session Duration') };
            case YAxis.CRASH_FREE:
                return { title: t('Crash Free Rate') };
            case YAxis.FAILED_TRANSACTIONS:
                return {
                    title: t('Failure Count'),
                    help: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
                };
            case YAxis.COUNT_DURATION:
                return { title: t('Slow Duration Count') };
            case YAxis.COUNT_VITAL:
                return { title: t('Slow Vital Count') };
            case YAxis.EVENTS:
            default:
                return { title: t('Event Count') };
        }
    };
    ReleaseChartContainer.prototype.cloneSeriesAsZero = function (series) {
        return __assign(__assign({}, series), { data: series.data.map(function (point) { return (__assign(__assign({}, point), { value: 0 })); }) });
    };
    ReleaseChartContainer.prototype.renderStackedChart = function () {
        var _a = this.props, location = _a.location, router = _a.router, organization = _a.organization, api = _a.api, releaseMeta = _a.releaseMeta, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, selection = _a.selection, version = _a.version;
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
        var eventView = getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization);
        var apiPayload = eventView.getEventsAPIPayload(location);
        var colors = this.getTransactionsChartColors();
        var _b = this.getChartTitle(), title = _b.title, help = _b.help;
        var releaseQueryExtra = {
            showTransactions: location.query.showTransactions,
            eventType: eventType,
            vitalType: vitalType,
            yAxis: yAxis,
        };
        return (<EventsChart router={router} organization={organization} showLegend yAxis={eventView.getYAxis()} query={apiPayload.query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} disablePrevious emphasizeReleases={[releaseMeta.version]} field={eventView.getFields()} topEvents={2} orderby={decodeScalar(apiPayload.sort)} currentSeriesName={t('This Release')} 
        // This seems a little strange but is intentional as EventsChart
        // uses the previousSeriesName as the secondary series name
        previousSeriesName={t('Other Releases')} seriesTransformer={this.seriesTransformer} disableableSeries={[t('This Release'), t('Other Releases')]} colors={colors} preserveReleaseQueryParams releaseQueryExtra={releaseQueryExtra} chartHeader={<HeaderTitleLegend>
            {title}
            {help && <QuestionTooltip size="sm" position="top" title={help}/>}
          </HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{ grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' } }}/>);
    };
    ReleaseChartContainer.prototype.renderHealthChart = function () {
        var _a = this.props, loading = _a.loading, errored = _a.errored, reloading = _a.reloading, chartData = _a.chartData, selection = _a.selection, yAxis = _a.yAxis, router = _a.router, platform = _a.platform;
        var _b = this.getChartTitle(), title = _b.title, help = _b.help;
        return (<HealthChartContainer platform={platform} loading={loading} errored={errored} reloading={reloading} chartData={chartData} selection={selection} yAxis={yAxis} router={router} title={title} help={help}/>);
    };
    ReleaseChartContainer.prototype.render = function () {
        var _a = this.props, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, hasDiscover = _a.hasDiscover, hasHealthData = _a.hasHealthData, hasPerformance = _a.hasPerformance, chartSummary = _a.chartSummary, onYAxisChange = _a.onYAxisChange, onEventTypeChange = _a.onEventTypeChange, onVitalTypeChange = _a.onVitalTypeChange, organization = _a.organization;
        var chart = null;
        if ((hasDiscover && yAxis === YAxis.EVENTS) ||
            (hasPerformance && PERFORMANCE_AXIS.includes(yAxis))) {
            chart = this.renderStackedChart();
        }
        else {
            chart = this.renderHealthChart();
        }
        return (<Panel>
        <ChartContainer>{chart}</ChartContainer>
        <ReleaseChartControls summary={chartSummary} yAxis={yAxis} onYAxisChange={onYAxisChange} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange} organization={organization} hasDiscover={hasDiscover} hasHealthData={hasHealthData} hasPerformance={hasPerformance}/>
      </Panel>);
    };
    return ReleaseChartContainer;
}(React.Component));
export default withTheme(ReleaseChartContainer);
//# sourceMappingURL=index.jsx.map