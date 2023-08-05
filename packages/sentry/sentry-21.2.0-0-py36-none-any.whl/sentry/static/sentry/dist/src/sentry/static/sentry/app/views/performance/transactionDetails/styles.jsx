import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import QuestionTooltip from 'app/components/questionTooltip';
import Tag, { Background } from 'app/components/tag';
import space from 'app/styles/space';
export function MetaData(_a) {
    var headingText = _a.headingText, tooltipText = _a.tooltipText, bodyText = _a.bodyText, subtext = _a.subtext;
    return (<Container>
      <StyledSectionHeading>
        {headingText}
        <QuestionTooltip position="top" size="sm" containerDisplayMode="block" title={tooltipText}/>
      </StyledSectionHeading>
      <SectionBody>{bodyText}</SectionBody>
      <SectionSubtext>{subtext}</SectionSubtext>
    </Container>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  min-width: 150px;\n"], ["\n  min-width: 150px;\n"])));
var StyledSectionHeading = styled(SectionHeading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var SectionBody = styled('p')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.headerFontSize; }, space(1));
var SectionSubtext = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export var NodesContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  height: 33px;\n  gap: ", ";\n\n  &:before {\n    content: '';\n    border-bottom: 1px solid ", ";\n    height: 33px;\n    position: absolute;\n    width: 100%;\n    transform: translateY(-50%);\n    z-index: ", ";\n  }\n"], ["\n  position: absolute;\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  height: 33px;\n  gap: ", ";\n\n  &:before {\n    content: '';\n    border-bottom: 1px solid ", ";\n    height: 33px;\n    position: absolute;\n    width: 100%;\n    transform: translateY(-50%);\n    z-index: ", ";\n  }\n"])), space(1), function (p) { return p.theme.gray500; }, function (p) { return p.theme.zIndex.initial; });
export var EventNode = styled(Tag)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  z-index: ", ";\n\n  & ", " {\n    border: 1px solid ", ";\n    height: 24px;\n    border-radius: 24px;\n  }\n"], ["\n  z-index: ", ";\n\n  & " /* sc-selector */, " {\n    border: 1px solid ", ";\n    height: 24px;\n    border-radius: 24px;\n  }\n"])), function (p) { return p.theme.zIndex.initial; }, /* sc-selector */ Background, function (p) { return p.theme.gray500; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=styles.jsx.map