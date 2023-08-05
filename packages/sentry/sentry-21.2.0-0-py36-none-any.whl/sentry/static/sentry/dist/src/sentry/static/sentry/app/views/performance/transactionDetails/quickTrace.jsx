import { __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { getTraceDateTimeRange } from 'app/components/events/interfaces/spans/utils';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { t, tn } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import { generateEventSlug } from 'app/utils/discover/urls';
import { getShortEventId } from 'app/utils/events';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import withProjects from 'app/utils/withProjects';
import { getTransactionDetailsUrl } from '../utils';
import QuickTraceQuery from './quickTraceQuery';
import { EventNode, MetaData, NodesContainer } from './styles';
import { isTransaction, parseTraceLite } from './utils';
export default function QuickTrace(_a) {
    var _b, _c, _d;
    var event = _a.event, location = _a.location, organization = _a.organization;
    // non transaction events are currently unsupported
    if (!isTransaction(event)) {
        return null;
    }
    var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : null;
    var traceTarget = generateTraceTarget(event, organization);
    return (<QuickTraceQuery event={event} location={location} orgSlug={organization.slug}>
      {function (_a) {
        var isLoading = _a.isLoading, error = _a.error, trace = _a.trace;
        var body = isLoading ? (<Placeholder height="33px"/>) : error || trace === null ? ('\u2014') : (<QuickTraceLite event={event} trace={trace} location={location} organization={organization}/>);
        return (<MetaData headingText={t('Quick Trace')} tooltipText={t('A minified version of the full trace.')} bodyText={body} subtext={traceId === null ? ('\u2014') : (<Link to={traceTarget}>
                  {t('Trace ID: %s', getShortEventId(traceId))}
                </Link>)}/>);
    }}
    </QuickTraceQuery>);
}
var QuickTraceLite = withProjects(function (_a) {
    var event = _a.event, trace = _a.trace, location = _a.location, organization = _a.organization, projects = _a.projects;
    // non transaction events are currently unsupported
    if (!isTransaction(event)) {
        return null;
    }
    var _b = parseTraceLite(trace, event), root = _b.root, current = _b.current, children = _b.children;
    var nodes = [];
    if (root) {
        var target = generateSingleEventTarget(root, organization, projects, location);
        nodes.push(<EventNode key="root" type="white" icon={null} to={target}>
          {t('Root')}
        </EventNode>);
    }
    var traceTarget = generateTraceTarget(event, organization);
    if (root && current && root.event_id !== current.parent_event_id) {
        nodes.push(<EventNode key="ancestors" type="white" icon={null} to={traceTarget}>
          {t('Ancestors')}
        </EventNode>);
    }
    nodes.push(<EventNode key="current" type="black">
        {t('This Event')}
      </EventNode>);
    if (children.length) {
        var childrenTarget = generateChildrenEventTarget(event, children, organization, projects, location);
        nodes.push(<EventNode key="children" type="white" icon={null} to={childrenTarget}>
          {tn('%s Child', '%s Children', children.length)}
        </EventNode>);
        nodes.push(<EventNode key="descendents" type="white" icon={null} to={traceTarget}>
          &nbsp;&nbsp;.&nbsp;&nbsp;.&nbsp;&nbsp;.&nbsp;&nbsp;
        </EventNode>);
    }
    return (<Container>
        <NodesContainer>{nodes}</NodesContainer>
      </Container>);
});
function generateSingleEventTarget(event, organization, projects, location) {
    var project = projects.find(function (p) { return parseInt(p.id, 10) === event.project_id; });
    if (project === undefined) {
        return undefined;
    }
    var eventSlug = generateEventSlug({
        id: event.event_id,
        project: project.slug,
    });
    return getTransactionDetailsUrl(organization, eventSlug, event.transaction, location.query);
}
function generateChildrenEventTarget(event, children, organization, projects, location) {
    if (children.length === 1) {
        return generateSingleEventTarget(children[0], organization, projects, location);
    }
    var queryResults = new QueryResults([]);
    var eventIds = children.map(function (child) { return child.event_id; });
    for (var i = 0; i < eventIds.length; i++) {
        queryResults.addOp(i === 0 ? '(' : 'OR');
        queryResults.addQuery("id:" + eventIds[i]);
        if (i === eventIds.length - 1) {
            queryResults.addOp(')');
        }
    }
    var _a = getTraceDateTimeRange({
        start: event.startTimestamp,
        end: event.endTimestamp,
    }), start = _a.start, end = _a.end;
    var traceEventView = EventView.fromSavedQuery({
        id: undefined,
        name: "Child Transactions of Event ID " + event.id,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: stringifyQueryObject(queryResults),
        projects: __spread(new Set(children.map(function (child) { return child.project_id; }))),
        version: 2,
        start: start,
        end: end,
    });
    return traceEventView.getResultsViewUrlTarget(organization.slug);
}
function generateTraceTarget(event, organization) {
    var _a, _b, _c;
    var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
    var _d = getTraceDateTimeRange({
        start: event.startTimestamp,
        end: event.endTimestamp,
    }), start = _d.start, end = _d.end;
    var eventView = EventView.fromSavedQuery({
        id: undefined,
        name: "Transactions with Trace ID " + traceId,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: "event.type:transaction trace:" + traceId,
        projects: [ALL_ACCESS_PROJECTS],
        version: 2,
        start: start,
        end: end,
    });
    return eventView.getResultsViewUrlTarget(organization.slug);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  height: 33px;\n"], ["\n  position: relative;\n  height: 33px;\n"])));
var templateObject_1;
//# sourceMappingURL=quickTrace.jsx.map