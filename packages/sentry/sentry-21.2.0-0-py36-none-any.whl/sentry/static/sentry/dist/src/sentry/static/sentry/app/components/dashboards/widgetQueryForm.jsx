import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getAggregateAlias } from 'app/utils/discover/fields';
import SearchBar from 'app/views/events/searchBar';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
import WidgetQueryFields from './widgetQueryFields';
var generateOrderOptions = function (fields) {
    var options = [];
    fields.forEach(function (field) {
        var alias = getAggregateAlias(field);
        options.push({ label: t('%s asc', field), value: alias });
        options.push({ label: t('%s desc', field), value: "-" + alias });
    });
    return options;
};
/**
 * Contain widget query interactions and signal changes via the onChange
 * callback. This component's state should live in the parent.
 */
var WidgetQueryForm = /** @class */ (function (_super) {
    __extends(WidgetQueryForm, _super);
    function WidgetQueryForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Handle scalar field values changing.
        _this.handleFieldChange = function (field) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            return function handleChange(value) {
                var _a;
                var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
                onChange(newQuery);
            };
        };
        _this.handleFieldsChange = function (fields) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            var newQuery = cloneDeep(widgetQuery);
            newQuery.fields = fields;
            onChange(newQuery);
        };
        return _this;
    }
    WidgetQueryForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, canRemove = _a.canRemove, displayType = _a.displayType, errors = _a.errors, fieldOptions = _a.fieldOptions, organization = _a.organization, selection = _a.selection, widgetQuery = _a.widgetQuery;
        return (<QueryWrapper>
        {canRemove && (<DeleteRow>
            <Button data-test-id="remove-query" size="xsmall" priority="danger" onClick={this.props.onRemove} icon={<IconDelete />}/>
          </DeleteRow>)}
        <Field data-test-id="new-query" label={t('Query')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.conditions} required>
          <SearchBar organization={organization} projectIds={selection.projects} query={widgetQuery.conditions} fields={[]} onSearch={this.handleFieldChange('conditions')} onBlur={this.handleFieldChange('conditions')} useFormWrapper={false}/>
        </Field>
        {canRemove && (<Field data-test-id="Query Name" label={t('Legend Alias')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.name}>
            <Input type="text" name="name" required value={widgetQuery.name} onChange={function (event) { return _this.handleFieldChange('name')(event.target.value); }}/>
          </Field>)}
        <WidgetQueryFields displayType={displayType} fieldOptions={fieldOptions} errors={errors} fields={widgetQuery.fields} onChange={this.handleFieldsChange}/>
        {displayType === 'table' && (<Field label={t('Sort by')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.orderby}>
            <SelectControl value={widgetQuery.orderby} name="orderby" options={generateOrderOptions(widgetQuery.fields)} onChange={function (option) {
            return _this.handleFieldChange('orderby')(option.value);
        }} onSelectResetsInput={false} onCloseResetsInput={false} onBlurResetsInput={false}/>
          </Field>)}
      </QueryWrapper>);
    };
    return WidgetQueryForm;
}(React.Component));
var QueryWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-bottom: ", ";\n  position: relative;\n"], ["\n  padding-bottom: ", ";\n  position: relative;\n"])), space(3));
var DeleteRow = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
export default WidgetQueryForm;
var templateObject_1, templateObject_2;
//# sourceMappingURL=widgetQueryForm.jsx.map