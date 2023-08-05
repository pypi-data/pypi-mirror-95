import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { components as selectComponents } from 'react-select';
import styled from '@emotion/styled';
import Badge from 'app/components/badge';
import NumberField from 'app/components/forms/numberField';
import SelectControl from 'app/components/forms/selectControl';
import TextField from 'app/components/forms/textField';
import { IconChevron, IconDocs } from 'app/icons';
import { t } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
import Aggregations from '../aggregations';
import Conditions from '../conditions';
import { NON_CONDITIONS_FIELDS } from '../data';
import { DiscoverDocs, DocsLabel, DocsLink, DocsSeparator, Fieldset, PlaceholderText, SidebarLabel, } from '../styles';
import { getOrderbyFields } from '../utils';
import Orderby from './orderby';
var QueryFields = /** @class */ (function (_super) {
    __extends(QueryFields, _super);
    function QueryFields() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getSummarizePlaceholder = function () {
            var queryBuilder = _this.props.queryBuilder;
            var query = queryBuilder.getInternal();
            var text = query.aggregations.length > 0
                ? t('Select fields')
                : t('No fields selected, showing all');
            return <PlaceholderText>{text}</PlaceholderText>;
        };
        _this.optionRenderer = function (_a) {
            var label = _a.label, data = _a.data, props = __rest(_a, ["label", "data"]);
            return (<selectComponents.Option label={label} data={data} {...props}>
        {label}
        {data.isTag && <Badge text="tag"/>}
      </selectComponents.Option>);
        };
        return _this;
    }
    QueryFields.prototype.render = function () {
        var _a = this.props, queryBuilder = _a.queryBuilder, onUpdateField = _a.onUpdateField, actions = _a.actions, isLoading = _a.isLoading, savedQuery = _a.savedQuery, savedQueryName = _a.savedQueryName, onUpdateName = _a.onUpdateName;
        var currentQuery = queryBuilder.getInternal();
        var columns = queryBuilder.getColumns();
        // Do not allow conditions on certain fields
        var columnsForConditions = columns.filter(function (_a) {
            var name = _a.name;
            return !NON_CONDITIONS_FIELDS.includes(name);
        });
        var fieldOptions = columns.map(function (_a) {
            var name = _a.name, isTag = _a.isTag;
            return ({
                value: name,
                label: name,
                isTag: isTag,
            });
        });
        return (<div>
        {savedQuery && (<Fieldset>
            <React.Fragment>
              <SidebarLabel htmlFor="name" className="control-label">
                {t('Name')}
              </SidebarLabel>
              <TextField name="name" value={getDynamicText({ value: savedQueryName, fixed: 'query name' })} placeholder={t('Saved search name')} onChange={function (val) {
            return onUpdateName && onUpdateName("" + val);
        }}/>
            </React.Fragment>
          </Fieldset>)}
        <Fieldset>
          <SidebarLabel htmlFor="fields" className="control-label">
            {t('Summarize')}
          </SidebarLabel>
          <SelectControl name="fields" multiple placeholder={this.getSummarizePlaceholder()} options={fieldOptions} components={{
            Option: this.optionRenderer,
        }} value={currentQuery.fields} onChange={function (val) {
            return onUpdateField('fields', val.map(function (_a) {
                var value = _a.value;
                return value;
            }));
        }} clearable disabled={isLoading} styles={{
            option: function (provided) {
                return __assign(__assign({}, provided), { display: 'flex', alignItems: 'center' });
            },
        }}/>
        </Fieldset>
        <Fieldset>
          <Aggregations value={currentQuery.aggregations} columns={columns} onChange={function (val) { return onUpdateField('aggregations', val); }} disabled={isLoading}/>
        </Fieldset>
        <Fieldset>
          <Conditions value={currentQuery.conditions} columns={columnsForConditions} onChange={function (val) { return onUpdateField('conditions', val); }} disabled={isLoading}/>
        </Fieldset>
        <Fieldset>
          <Orderby value={currentQuery.orderby} columns={getOrderbyFields(queryBuilder)} onChange={function (val) { return onUpdateField('orderby', val); }} disabled={isLoading}/>
        </Fieldset>
        <Fieldset>
          <NumberField name="limit" label={<SidebarLabel>{t('Limit')}</SidebarLabel>} placeholder="#" value={currentQuery.limit} onChange={function (val) {
            return onUpdateField('limit', typeof val === 'number' ? val : null);
        }} disabled={isLoading}/>
        </Fieldset>
        <Fieldset>{actions}</Fieldset>
        <DocsSeparator />
        <DocsLink href="https://docs.sentry.io/product/discover/">
          <DiscoverDocs>
            <IconDocs size="sm"/>
            <DocsLabel>{t('Discover Documentation')}</DocsLabel>
            <StyledIconChevron direction="right" size="1em"/>
          </DiscoverDocs>
        </DocsLink>
      </div>);
    };
    return QueryFields;
}(React.Component));
export default QueryFields;
var StyledIconChevron = styled(IconChevron)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var templateObject_1;
//# sourceMappingURL=queryFields.jsx.map