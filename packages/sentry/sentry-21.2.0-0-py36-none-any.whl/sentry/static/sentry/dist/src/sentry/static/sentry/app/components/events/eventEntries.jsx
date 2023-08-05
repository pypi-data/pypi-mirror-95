import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ErrorBoundary from 'app/components/errorBoundary';
import EventContexts from 'app/components/events/contexts';
import EventContextSummary from 'app/components/events/contextSummary/contextSummary';
import EventDevice from 'app/components/events/device';
import EventErrors from 'app/components/events/errors';
import EventAttachments from 'app/components/events/eventAttachments';
import EventCause from 'app/components/events/eventCause';
import EventCauseEmpty from 'app/components/events/eventCauseEmpty';
import EventDataSection from 'app/components/events/eventDataSection';
import EventExtraData from 'app/components/events/eventExtraData/eventExtraData';
import EventSdk from 'app/components/events/eventSdk';
import EventTags from 'app/components/events/eventTags/eventTags';
import EventGroupingInfo from 'app/components/events/groupingInfo';
import EventPackageData from 'app/components/events/packageData';
import RRWebIntegration from 'app/components/events/rrwebIntegration';
import EventSdkUpdates from 'app/components/events/sdkUpdates';
import { DataSection } from 'app/components/events/styles';
import EventUserFeedback from 'app/components/events/userFeedback';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isNotSharedOrganization } from 'app/types/utils';
import { objectIsEmpty } from 'app/utils';
import { analytics } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
import EventEntry from './eventEntry';
var defaultProps = {
    isShare: false,
    showExampleCommit: false,
    showTagSummary: true,
};
var EventEntries = /** @class */ (function (_super) {
    __extends(EventEntries, _super);
    function EventEntries() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventEntries.prototype.componentDidMount = function () {
        var event = this.props.event;
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        var errors = event.errors;
        var errorTypes = errors.map(function (errorEntries) { return errorEntries.type; });
        var errorMessages = errors.map(function (errorEntries) { return errorEntries.message; });
        this.recordIssueError(errorTypes, errorMessages);
    };
    EventEntries.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, event = _a.event, showExampleCommit = _a.showExampleCommit;
        return ((event && nextProps.event && event.id !== nextProps.event.id) ||
            showExampleCommit !== nextProps.showExampleCommit);
    };
    EventEntries.prototype.recordIssueError = function (errorTypes, errorMessages) {
        var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
        var orgId = organization.id;
        var platform = project.platform;
        analytics('issue_error_banner.viewed', __assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform: platform })));
    };
    EventEntries.prototype.renderEntries = function () {
        var _a = this.props, event = _a.event, project = _a.project, organization = _a.organization, isShare = _a.isShare;
        var entries = event === null || event === void 0 ? void 0 : event.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map(function (entry, entryIdx) { return (<ErrorBoundary key={"entry-" + entryIdx} customComponent={<EventDataSection type={entry.type} title={entry.type}>
            <p>{t('There was an error rendering this data.')}</p>
          </EventDataSection>}>
        <EventEntry projectSlug={project.slug} organization={organization} event={event} entry={entry} isShare={isShare}/>
      </ErrorBoundary>); });
    };
    EventEntries.prototype.render = function () {
        var _a = this.props, className = _a.className, organization = _a.organization, group = _a.group, isShare = _a.isShare, project = _a.project, event = _a.event, showExampleCommit = _a.showExampleCommit, showTagSummary = _a.showTagSummary, location = _a.location;
        var features = organization && organization.features ? new Set(organization.features) : new Set();
        var hasQueryFeature = features.has('discover-query');
        if (!event) {
            return (<div style={{ padding: '15px 30px' }}>
          <h3>{t('Latest Event Not Available')}</h3>
        </div>);
        }
        var hasContext = !objectIsEmpty(event.user) || !objectIsEmpty(event.contexts);
        var hasErrors = !objectIsEmpty(event.errors);
        return (<div className={className} data-test-id="event-entries">
        {hasErrors && (<ErrorContainer>
            <EventErrors event={event} orgSlug={organization.slug} projectSlug={project.slug}/>
          </ErrorContainer>)}
        {!isShare &&
            isNotSharedOrganization(organization) &&
            (showExampleCommit ? (<EventCauseEmpty organization={organization} project={project}/>) : (<EventCause organization={organization} project={project} event={event} group={group}/>))}
        {(event === null || event === void 0 ? void 0 : event.userReport) && group && (<StyledEventUserFeedback report={event.userReport} orgId={organization.slug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {hasContext && showTagSummary && <EventContextSummary event={event}/>}
        {showTagSummary && (<EventTags event={event} organization={organization} projectId={project.slug} location={location} hasQueryFeature={hasQueryFeature}/>)}
        {this.renderEntries()}
        {hasContext && <EventContexts group={group} event={event}/>}
        {event && !objectIsEmpty(event.context) && <EventExtraData event={event}/>}
        {event && !objectIsEmpty(event.packages) && <EventPackageData event={event}/>}
        {event && !objectIsEmpty(event.device) && <EventDevice event={event}/>}
        {!isShare && features.has('event-attachments') && (<EventAttachments event={event} orgId={organization.slug} projectId={project.slug} location={location}/>)}
        {(event === null || event === void 0 ? void 0 : event.sdk) && !objectIsEmpty(event.sdk) && <EventSdk sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<EventSdkUpdates event={__assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && (event === null || event === void 0 ? void 0 : event.groupID) && (<EventGroupingInfo projectId={project.slug} event={event} showGroupingConfig={features.has('set-grouping-config')}/>)}
        {!isShare && features.has('event-attachments') && (<RRWebIntegration event={event} orgId={organization.slug} projectId={project.slug}/>)}
      </div>);
    };
    EventEntries.defaultProps = defaultProps;
    return EventEntries;
}(React.Component));
var ErrorContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"], ["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"])));
var BorderlessEventEntries = styled(EventEntries)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & ", " {\n    padding: ", " 0 0 0;\n  }\n  & ", ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & ", " {\n    margin-bottom: ", ";\n  }\n"], ["\n  & " /* sc-selector */, " {\n    padding: ", " 0 0 0;\n  }\n  & " /* sc-selector */, ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & " /* sc-selector */, " {\n    margin-bottom: ", ";\n  }\n"])), /* sc-selector */ DataSection, space(3), /* sc-selector */ DataSection, /* sc-selector */ ErrorContainer, space(2));
var StyledEventUserFeedback = styled(EventUserFeedback)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"], ["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"])), function (p) { return (p.includeBorder ? "border-top: 1px solid " + p.theme.innerBorder + ";" : ''); });
// TODO(ts): any required due to our use of SharedViewOrganization
export default withOrganization(EventEntries);
export { BorderlessEventEntries };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventEntries.jsx.map