import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DynamicSamplingInnerName } from 'app/types/dynamicSampling';
import SelectField from 'app/views/settings/components/forms/selectField';
import TextareaField from 'app/views/settings/components/forms/textareaField';
import LegacyBrowsersField from './legacyBrowsersField';
function ConditionFields(_a) {
    var conditions = _a.conditions, categoryOptions = _a.categoryOptions, onAdd = _a.onAdd, onDelete = _a.onDelete, onChange = _a.onChange;
    return (<Wrapper>
      {conditions.map(function (_a, index) {
        var match = _a.match, category = _a.category;
        var showLegacyBrowsers = category === DynamicSamplingInnerName.LEGACY_BROWSERS;
        return (<FieldsWrapper key={index}>
            <Fields>
              <SelectField label={t('Category')} 
        // help={t('This is a description')} // TODO(PRISCILA): Add correct description
        name={"category-" + index} value={category} onChange={function (value) { return onChange(index, 'category', value); }} choices={categoryOptions} inline={false} hideControlState showHelpInTooltip required stacked/>
              <TextareaField label={t('Matches')} 
        // help={t('This is a description')} // TODO(PRISCILA): Add correct description
        placeholder={showLegacyBrowsers
            ? t('No match')
            : t('%s (Multiline)', 'ex. 1* or [I3].[0-9].*')} name={"match-" + index} value={match} onChange={function (value) { return onChange(index, 'match', value); }} disabled={showLegacyBrowsers} inline={false} autosize hideControlState showHelpInTooltip flexibleControlStateSize required stacked/>
              <ButtonDeleteWrapper>
                <Button onClick={onDelete(index)} size="small">
                  {t('Delete Condition')}
                </Button>
              </ButtonDeleteWrapper>
            </Fields>
            <IconDeleteWrapper onClick={onDelete(index)}>
              <IconDelete aria-label={t('Delete Condition')}/>
            </IconDeleteWrapper>
            {showLegacyBrowsers && (<LegacyBrowsersField onChange={function (value) {
            onChange(index, 'legacyBrowsers', value);
        }}/>)}
          </FieldsWrapper>);
    })}
      <StyledButton icon={<IconAdd isCircled/>} onClick={onAdd} size="small">
        {t('Add Condition')}
      </StyledButton>
    </Wrapper>);
}
export default ConditionFields;
var IconDeleteWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 40px;\n  margin-top: 24px;\n  cursor: pointer;\n  display: none;\n  align-items: center;\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"], ["\n  height: 40px;\n  margin-top: 24px;\n  cursor: pointer;\n  display: none;\n  align-items: center;\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var Fields = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr;\n    grid-gap: ", ";\n  }\n"], ["\n  display: grid;\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr;\n    grid-gap: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(2));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  > * {\n    :not(:first-child) {\n      label {\n        display: none;\n      }\n      ", " {\n        margin-top: 0;\n      }\n\n      ", " {\n        @media (max-width: ", ") {\n          border-top: 1px solid ", ";\n          padding-top: ", ";\n          margin-top: ", ";\n        }\n      }\n    }\n  }\n"], ["\n  > * {\n    :not(:first-child) {\n      label {\n        display: none;\n      }\n      ", " {\n        margin-top: 0;\n      }\n\n      ", " {\n        @media (max-width: ", ") {\n          border-top: 1px solid ", ";\n          padding-top: ", ";\n          margin-top: ", ";\n        }\n      }\n    }\n  }\n"])), IconDeleteWrapper, Fields, function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.border; }, space(2), space(2));
var FieldsWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var ButtonDeleteWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var StyledButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: ", " 0;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"], ["\n  margin: ", " 0;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=conditionFields.jsx.map