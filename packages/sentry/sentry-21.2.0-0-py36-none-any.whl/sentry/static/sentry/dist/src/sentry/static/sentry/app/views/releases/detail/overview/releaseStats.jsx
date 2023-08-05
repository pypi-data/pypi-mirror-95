import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { SectionHeading } from 'app/components/charts/styles';
import Count from 'app/components/count';
import DeployBadge from 'app/components/deployBadge';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import NotAvailable from 'app/components/notAvailable';
import ProgressBar from 'app/components/progressBar';
import QuestionTooltip from 'app/components/questionTooltip';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import NOT_AVAILABLE_MESSAGES from 'app/constants/notAvailableMessages';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
import { getSessionTermDescription, SessionTerm, sessionTerm, } from 'app/views/releases/utils/sessionTerm';
import AdoptionTooltip from '../../list/adoptionTooltip';
import CrashFree from '../../list/crashFree';
import { getReleaseNewIssuesUrl, getReleaseUnhandledIssuesUrl } from '../../utils';
import { getReleaseEventView } from '../utils';
function ReleaseStats(_a) {
    var _b;
    var organization = _a.organization, release = _a.release, project = _a.project, location = _a.location, selection = _a.selection;
    var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, newGroups = release.newGroups, version = release.version;
    var hasHealthData = project.hasHealthData, healthData = project.healthData;
    var sessionsCrashed = healthData.sessionsCrashed, adoption = healthData.adoption, crashFreeUsers = healthData.crashFreeUsers, crashFreeSessions = healthData.crashFreeSessions, totalUsers = healthData.totalUsers, totalUsers24h = healthData.totalUsers24h, totalSessions = healthData.totalSessions, totalSessions24h = healthData.totalSessions24h;
    return (<Container>
      <div>
        <SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Date Deployed') : t('Date Created')}
        </SectionHeading>
        <div>
          <TimeSince date={(_b = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _b !== void 0 ? _b : dateCreated}/>
        </div>
      </div>

      <div>
        <SectionHeading>{t('Last Deploy')}</SectionHeading>
        <div>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<DeployBadge deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<NotAvailable />)}
        </div>
      </div>

      <div>
        <SectionHeading>{t('Crash Free Sessions')}</SectionHeading>
        <div>
          {defined(crashFreeSessions) ? (<CrashFree percent={crashFreeSessions} iconSize="md"/>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
        </div>
      </div>

      <div>
        <SectionHeading>{t('Crash Free Users')}</SectionHeading>
        <div>
          {defined(crashFreeUsers) ? (<CrashFree percent={crashFreeUsers} iconSize="md"/>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
        </div>
      </div>

      <AdoptionWrapper>
        <SectionHeading>{t('User Adoption')}</SectionHeading>
        {defined(adoption) ? (<Tooltip containerDisplayMode="block" title={<AdoptionTooltip totalUsers={totalUsers} totalSessions={totalSessions} totalUsers24h={totalUsers24h} totalSessions24h={totalSessions24h}/>}>
            <ProgressBar value={Math.ceil(adoption)}/>
          </Tooltip>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
      </AdoptionWrapper>

      <LinkedStatsWrapper>
        <div>
          <SectionHeading>{t('New Issues')}</SectionHeading>
          <div>
            <Tooltip title={t('Open in Issues')}>
              <GlobalSelectionLink to={getReleaseNewIssuesUrl(organization.slug, project.id, version)}>
                <Count value={newGroups}/>
              </GlobalSelectionLink>
            </Tooltip>
          </div>
        </div>

        <div>
          <SectionHeading>
            {sessionTerm.crashes}
            <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASHES, project.platform)} size="sm"/>
          </SectionHeading>
          <div>
            {hasHealthData ? (<Tooltip title={t('Open in Issues')}>
                <GlobalSelectionLink to={getReleaseUnhandledIssuesUrl(organization.slug, project.id, version)}>
                  <Count value={sessionsCrashed}/>
                </GlobalSelectionLink>
              </Tooltip>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
          </div>
        </div>

        <div>
          <SectionHeading>
            {t('Apdex')}
            <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.APDEX)} size="sm"/>
          </SectionHeading>
          <div>
            <Feature features={['performance-view']}>
              {function (hasFeature) {
        return hasFeature ? (<DiscoverQuery eventView={getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                    {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            if (isLoading ||
                error ||
                !tableData ||
                tableData.data.length === 0) {
                return <NotAvailable />;
            }
            return (<GlobalSelectionLink to={{
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: {
                    query: "release:" + (release === null || release === void 0 ? void 0 : release.version),
                },
            }}>
                          <Tooltip title={t('Open in Performance')}>
                            <Count value={tableData.data[0][getAggregateAlias("apdex(" + organization.apdexThreshold + ")")]}/>
                          </Tooltip>
                        </GlobalSelectionLink>);
        }}
                  </DiscoverQuery>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.performance}/>);
    }}
            </Feature>
          </div>
        </div>
      </LinkedStatsWrapper>
    </Container>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"])), space(2), space(3));
var LinkedStatsWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"])));
var AdoptionWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
export default ReleaseStats;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseStats.jsx.map