import { __read, __spread } from "tslib";
import React from 'react';
import moment from 'moment';
import MarkLine from 'app/components/charts/components/markLine';
import LineChart from 'app/components/charts/lineChart';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var MetricChart = function (_a) {
    var data = _a.data, incidents = _a.incidents;
    // Iterate through incidents to add markers to chart
    var series = __spread(data);
    var dataArr = data[0].data;
    var firstPoint = Number(dataArr[0].name);
    var lastPoint = dataArr[dataArr.length - 1].name;
    var resolvedArea = {
        seriesName: 'Critical Area',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: theme.green300, type: 'solid', width: 4 },
            data: [[{ coord: [firstPoint, 0] }, { coord: [lastPoint, 0] }]],
        }),
        data: [],
    };
    series.push(resolvedArea);
    if (incidents) {
        // select incidents that fall within the graph range
        var periodStart_1 = moment.utc(firstPoint);
        var filteredIncidents = incidents.filter(function (incident) {
            return !incident.dateClosed || moment(incident.dateClosed).isAfter(periodStart_1);
        });
        var criticalLines = filteredIncidents.map(function (incident) {
            var detectTime = Math.max(moment(incident.dateStarted).valueOf(), firstPoint);
            var resolveTime;
            if (incident.dateClosed) {
                resolveTime = moment(incident.dateClosed).valueOf();
            }
            else {
                resolveTime = lastPoint;
            }
            var line = [{ coord: [detectTime, 0] }, { coord: [resolveTime, 0] }];
            return line;
        });
        var criticalArea = {
            seriesName: 'Critical Area',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.red300, type: 'solid', width: 4 },
                data: criticalLines,
            }),
            data: [],
        };
        series.push(criticalArea);
        var incidentValueMap_1 = {};
        var incidentLines = filteredIncidents.map(function (_a) {
            var dateStarted = _a.dateStarted, id = _a.id;
            var incidentStart = moment(dateStarted).valueOf();
            incidentValueMap_1[incidentStart] = id;
            return { xAxis: incidentStart };
        });
        var incidentLinesSeries = {
            seriesName: 'Incident Line',
            type: 'line',
            markLine: MarkLine({
                silent: true,
                lineStyle: { color: theme.red300, type: 'solid' },
                data: incidentLines,
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: function (_a) {
                        var _b;
                        var value = _a.value;
                        return (_b = incidentValueMap_1[value]) !== null && _b !== void 0 ? _b : '-';
                    },
                    color: theme.red300,
                    fontSize: 10,
                },
            }),
            data: [],
        };
        series.push(incidentLinesSeries);
    }
    return (<LineChart isGroupedByDate showTimeInTooltip grid={{
        left: 0,
        right: 0,
        top: space(2),
        bottom: 0,
    }} series={series}/>);
};
export default MetricChart;
//# sourceMappingURL=metricChart.jsx.map