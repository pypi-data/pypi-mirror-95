import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import PanelTable from 'app/components/panels/panelTable';
import QuestionTooltip from 'app/components/questionTooltip';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import Candidate from './candidate';
function Candidates(_a) {
    var candidates = _a.candidates, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, builtinSymbolSources = _a.builtinSymbolSources, onDelete = _a.onDelete, isLoading = _a.isLoading;
    return (<Wrapper>
      <Title>
        {t('Debug Files')}
        <QuestionTooltip title={tct('These are the Debug Information Files (DIFs) corresponding to this image which have been looked up on [docLink:symbol servers] during the processing of the stacktrace.', {
        docLink: (<ExternalLink href="https://docs.sentry.io/platforms/native/data-management/debug-files/#symbol-servers"/>),
    })} size="xs" position="top" isHoverable/>
      </Title>
      <StyledPanelTable headers={[
        t('Status'),
        t('Debug File'),
        t('Processing'),
        t('Features'),
        t('Actions'),
    ]} isEmpty={!candidates.length} isLoading={isLoading} emptyMessage={t('There are no debug files to display')}>
        {candidates.map(function (candidate, index) { return (<Candidate key={index} candidate={candidate} builtinSymbolSources={builtinSymbolSources} organization={organization} baseUrl={baseUrl} projectId={projectId} onDelete={onDelete}/>); })}
      </StyledPanelTable>
    </Wrapper>);
}
export default Candidates;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var StyledPanelTable = styled(PanelTable)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-template-columns: 0.5fr minmax(300px, 2fr) 1fr 1fr;\n\n  > *:nth-child(5n) {\n    padding: 0;\n    display: none;\n  }\n\n  > *:nth-child(5n-1),\n  > *:nth-child(5n) {\n    text-align: right;\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    overflow: visible;\n    > *:nth-child(5n-1) {\n      text-align: left;\n      justify-content: flex-start;\n    }\n\n    > *:nth-child(5n) {\n      padding: ", ";\n      display: flex;\n    }\n\n    grid-template-columns: 1fr minmax(300px, 2.5fr) 1.5fr 1.5fr 0.5fr;\n  }\n"], ["\n  grid-template-columns: 0.5fr minmax(300px, 2fr) 1fr 1fr;\n\n  > *:nth-child(5n) {\n    padding: 0;\n    display: none;\n  }\n\n  > *:nth-child(5n-1),\n  > *:nth-child(5n) {\n    text-align: right;\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    overflow: visible;\n    > *:nth-child(5n-1) {\n      text-align: left;\n      justify-content: flex-start;\n    }\n\n    > *:nth-child(5n) {\n      padding: ", ";\n      display: flex;\n    }\n\n    grid-template-columns: 1fr minmax(300px, 2.5fr) 1.5fr 1.5fr 0.5fr;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; }, space(2));
// Table Title
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.gray400; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=candidates.jsx.map