import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import pick from 'lodash/pick';
import set from 'lodash/set';
import { validateWidget } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import WidgetQueryForm from 'app/components/dashboards/widgetQueryForm';
import SelectControl from 'app/components/forms/selectControl';
import { PanelAlert } from 'app/components/panels';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isAggregateField } from 'app/utils/discover/fields';
import Measurements from 'app/utils/measurements/measurements';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withTags from 'app/utils/withTags';
import { DISPLAY_TYPE_CHOICES } from 'app/views/dashboardsV2/data';
import WidgetCard from 'app/views/dashboardsV2/widgetCard';
import { generateFieldOptions } from 'app/views/eventsV2/utils';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
var newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
function mapErrors(data, update) {
    Object.keys(data).forEach(function (key) {
        var value = data[key];
        // Recurse into nested objects.
        if (Array.isArray(value) && typeof value[0] === 'string') {
            update[key] = value[0];
        }
        else if (Array.isArray(value) && typeof value[0] === 'object') {
            update[key] = value.map(function (item) { return mapErrors(item, {}); });
        }
        else {
            update[key] = mapErrors(value, {});
        }
    });
    return update;
}
var AddDashboardWidgetModal = /** @class */ (function (_super) {
    __extends(AddDashboardWidgetModal, _super);
    function AddDashboardWidgetModal(props) {
        var _this = _super.call(this, props) || this;
        _this.handleSubmit = function (event) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, onAddWidget, onUpdateWidget, previousWidget, widgetData, err_1, errors;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        event.preventDefault();
                        _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, onAddWidget = _a.onAddWidget, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, 4, 5]);
                        widgetData = pick(this.state, [
                            'title',
                            'displayType',
                            'interval',
                            'queries',
                        ]);
                        return [4 /*yield*/, validateWidget(api, organization.slug, widgetData)];
                    case 2:
                        _c.sent();
                        if (typeof onUpdateWidget === 'function' && !!previousWidget) {
                            onUpdateWidget(__assign({ id: previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.id }, widgetData));
                            addSuccessMessage(t('Updated widget.'));
                        }
                        else {
                            onAddWidget(widgetData);
                            addSuccessMessage(t('Added widget.'));
                        }
                        closeModal();
                        return [3 /*break*/, 5];
                    case 3:
                        err_1 = _c.sent();
                        errors = mapErrors((_b = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) !== null && _b !== void 0 ? _b : {}, {});
                        this.setState({ errors: errors });
                        return [3 /*break*/, 5];
                    case 4:
                        this.setState({ loading: false });
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFieldChange = function (field) { return function (value) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, field, value);
                if (field === 'displayType') {
                    var newQueries = prevState.queries;
                    if (['table', 'world_map', 'big_number'].includes(value)) {
                        // Some display types may only support at most 1 query.
                        set(newState, 'queries', prevState.queries.slice(0, 1));
                        newQueries = newState.queries;
                    }
                    if (value === 'table') {
                        return newState;
                    }
                    // Filter out non-aggregate fields
                    newQueries = newQueries.map(function (query) {
                        var fields = query.fields.filter(isAggregateField);
                        return __assign(__assign({}, query), { fields: fields.length ? fields : ['count()'] });
                    });
                    if (['world_map', 'big_number'].includes(value)) {
                        // For world map chart, cap fields of the queries to only one field.
                        newQueries = newQueries.map(function (query) {
                            return __assign(__assign({}, query), { fields: query.fields.slice(0, 1) });
                        });
                    }
                    set(newState, 'queries', newQueries);
                }
                return newState;
            });
        }; };
        _this.handleQueryChange = function (widgetQuery, index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, "queries." + index, widgetQuery);
                return newState;
            });
        };
        _this.handleQueryRemove = function (index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                newState.queries.splice(index, index + 1);
                // If there is only one query, then its name will not be visible.
                if (newState.queries.length === 1) {
                    newState.queries[0].name = '';
                }
                return newState;
            });
        };
        _this.handleAddOverlay = function () {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                newState.queries.push(cloneDeep(newQuery));
                return newState;
            });
        };
        var widget = props.widget;
        if (!widget) {
            _this.state = {
                title: '',
                displayType: 'line',
                interval: '5m',
                queries: [__assign({}, newQuery)],
                errors: undefined,
                loading: false,
            };
            return _this;
        }
        _this.state = {
            title: widget.title,
            displayType: widget.displayType,
            interval: widget.interval,
            queries: widget.queries,
            errors: undefined,
            loading: false,
        };
        return _this;
    }
    AddDashboardWidgetModal.prototype.canAddOverlay = function () {
        return ['line', 'area', 'stacked_area', 'bar'].includes(this.state.displayType);
    };
    AddDashboardWidgetModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Footer = _a.Footer, Body = _a.Body, Header = _a.Header, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, selection = _a.selection, tags = _a.tags, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
        var state = this.state;
        var errors = state.errors;
        var fieldOptions = function (measurementKeys) {
            return generateFieldOptions({
                organization: organization,
                tagKeys: Object.values(tags).map(function (_a) {
                    var key = _a.key;
                    return key;
                }),
                measurementKeys: measurementKeys,
            });
        };
        var isUpdatingWidget = typeof onUpdateWidget === 'function' && !!previousWidget;
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          <h4>{isUpdatingWidget ? t('Edit Widget') : t('Add Widget')}</h4>
        </Header>
        <Body>
          <DoubleFieldWrapper>
            <Field data-test-id="widget-name" label={t('Widget Name')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.title} required>
              <Input type="text" name="title" maxLength={255} required value={state.title} onChange={function (event) {
            _this.handleFieldChange('title')(event.target.value);
        }}/>
            </Field>
            <Field data-test-id="chart-type" label={t('Visualization Display')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.displayType} required>
              <SelectControl required options={DISPLAY_TYPE_CHOICES.slice()} name="displayType" label={t('Visualization Display')} value={state.displayType} onChange={function (option) {
            _this.handleFieldChange('displayType')(option.value);
        }}/>
            </Field>
          </DoubleFieldWrapper>
          <Measurements>
            {function (_a) {
            var measurements = _a.measurements;
            var measurementKeys = Object.values(measurements).map(function (_a) {
                var key = _a.key;
                return key;
            });
            var amendedFieldOptions = fieldOptions(measurementKeys);
            return (<React.Fragment>
                  {state.queries.map(function (query, i) {
                var _a;
                return (<WidgetQueryForm key={i} api={api} organization={organization} selection={selection} fieldOptions={amendedFieldOptions} displayType={state.displayType} widgetQuery={query} canRemove={state.queries.length > 1} onRemove={function () { return _this.handleQueryRemove(i); }} onChange={function (widgetQuery) {
                    return _this.handleQueryChange(widgetQuery, i);
                }} errors={(_a = errors === null || errors === void 0 ? void 0 : errors.queries) === null || _a === void 0 ? void 0 : _a[i]}/>);
            })}
                </React.Fragment>);
        }}
          </Measurements>
          {this.canAddOverlay() && (<AddOverlayButton icon={<IconAdd isCircled/>} onClick={function (event) {
            event.preventDefault();
            _this.handleAddOverlay();
        }}>
              {t('New Query Overlay')}
            </AddOverlayButton>)}
          <WidgetCard api={api} organization={organization} selection={selection} widget={this.state} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
            return typeof errorMessage === 'string' && (<PanelAlert type="error">{errorMessage}</PanelAlert>);
        }} isSorting={false} currentWidgetDragging={false}/>
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button external href="https://docs.sentry.io/product/dashboards/">
              {t('Read the docs')}
            </Button>
            <Button data-test-id="add-widget" priority="primary" type="button" onClick={this.handleSubmit} disabled={state.loading} busy={state.loading}>
              {isUpdatingWidget ? t('Update Widget') : t('Add Widget')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return AddDashboardWidgetModal;
}(React.Component));
var DoubleFieldWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"])), space(1));
var AddOverlayButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
export default withApi(withGlobalSelection(withTags(AddDashboardWidgetModal)));
var templateObject_1, templateObject_2;
//# sourceMappingURL=addDashboardWidgetModal.jsx.map