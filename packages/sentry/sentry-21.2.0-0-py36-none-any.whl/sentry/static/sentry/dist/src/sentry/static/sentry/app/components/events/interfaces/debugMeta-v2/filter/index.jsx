import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import DropdownControl from 'app/components/dropdownControl';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t } from 'app/locale';
import space from 'app/styles/space';
import DropDownButton from './dropDownButton';
function Filter(_a) {
    var options = _a.options, onFilter = _a.onFilter;
    function handleClick(option) {
        return function () {
            var updatedOptions = options.map(function (opt) {
                if (option.id === opt.id) {
                    return __assign(__assign({}, opt), { isChecked: !opt.isChecked });
                }
                return opt;
            });
            onFilter(updatedOptions);
        };
    }
    var checkedQuantity = options.filter(function (option) { return option.isChecked; }).length;
    return (<Wrapper>
      <DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
        var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
        return (<DropDownButton isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>);
    }}>
        <Header>{t('Status')}</Header>
        <List>
          {options.map(function (option) {
        var symbol = option.symbol, isChecked = option.isChecked, id = option.id;
        return (<StyledListItem key={id} onClick={handleClick(option)} isChecked={isChecked}>
                {symbol}
                <CheckboxFancy isChecked={isChecked}/>
              </StyledListItem>);
    })}
        </List>
      </DropdownControl>
    </Wrapper>);
}
export default Filter;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var StyledListItem = styled(ListItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  :not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  :not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return p.theme.blue300; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map