import { __assign, __rest } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import EventView from 'app/utils/discover/eventView';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
import { isTransaction } from './utils';
function getQuickTraceRequestPayload(_a) {
    var eventView = _a.eventView, event = _a.event, location = _a.location;
    var additionalApiPayload = omit(eventView.getEventsAPIPayload(location), [
        'field',
        'sort',
        'per_page',
    ]);
    return Object.assign({ event_id: event.id }, additionalApiPayload);
}
function beforeFetch(api) {
    api.clear();
}
function makeEventView(event) {
    var _a = getTraceDateTimeRange({
        start: event.startTimestamp,
        end: event.endTimestamp,
    }), start = _a.start, end = _a.end;
    return EventView.fromSavedQuery({
        id: undefined,
        version: 2,
        name: '',
        // This field doesn't actually do anything,
        // just here to satify a constraint in EventView.
        fields: ['transaction.duration'],
        projects: [ALL_ACCESS_PROJECTS],
        query: '',
        environment: [],
        range: '',
        start: start,
        end: end,
    });
}
function EmptyTrace(_a) {
    var children = _a.children;
    return (<React.Fragment>
      {children({
        isLoading: true,
        error: null,
        pageLinks: null,
        trace: null,
    })}
    </React.Fragment>);
}
function QuickTraceQuery(_a) {
    var _b, _c;
    var event = _a.event, children = _a.children, props = __rest(_a, ["event", "children"]);
    // non transaction events are currently unsupported
    if (!isTransaction(event)) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var traceId = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var eventView = makeEventView(event);
    return (<GenericDiscoverQuery event={event} route={"events-trace-light/" + traceId} getRequestPayload={getQuickTraceRequestPayload} beforeFetch={beforeFetch} eventView={eventView} {...props}>
      {function (_a) {
        var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
        return children(__assign({ trace: tableData !== null && tableData !== void 0 ? tableData : null }, rest));
    }}
    </GenericDiscoverQuery>);
}
export default withApi(QuickTraceQuery);
//# sourceMappingURL=quickTraceQuery.jsx.map