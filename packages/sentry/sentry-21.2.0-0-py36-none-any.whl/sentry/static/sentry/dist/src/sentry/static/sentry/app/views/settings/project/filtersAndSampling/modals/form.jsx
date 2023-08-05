import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DynamicSamplingInnerName, DynamicSamplingInnerOperator, } from 'app/types/dynamicSampling';
import { defined } from 'app/utils';
import NumberField from 'app/views/settings/components/forms/numberField';
import RadioField from 'app/views/settings/components/forms/radioField';
import ConditionFields from './conditionFields';
import handleXhrErrorResponse from './handleXhrErrorResponse';
import { Transaction } from './utils';
var transactionChoices = [
    [Transaction.ALL, t('All')],
    [Transaction.MATCH_CONDITIONS, t('Match Conditions')],
];
var Form = /** @class */ (function (_super) {
    __extends(Form, _super);
    function Form() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            _this.setState(function (prevState) {
                var _a;
                return (__assign(__assign({}, prevState), (_a = {}, _a[field] = value, _a)));
            });
        };
        _this.handleSubmit = function () {
            // Children have to implement this
            throw new Error('Not implemented');
        };
        _this.handleAddCondition = function () {
            // Children have to implement this
            throw new Error('Not implemented');
        };
        _this.handleChangeCondition = function (index, field, value) {
            var newConditions = __spread(_this.state.conditions);
            newConditions[index][field] = value;
            _this.setState({ conditions: newConditions });
        };
        _this.handleDeleteCondition = function (index) { return function () {
            var newConditions = __spread(_this.state.conditions);
            newConditions.splice(index, 1);
            if (!newConditions.length) {
                _this.setState({
                    conditions: newConditions,
                    transaction: Transaction.ALL,
                });
                return;
            }
            _this.setState({ conditions: newConditions });
        }; };
        return _this;
    }
    Form.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.transaction === Transaction.ALL &&
            this.state.transaction !== Transaction.ALL &&
            !this.state.conditions.length) {
            this.handleAddCondition();
        }
    };
    Form.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        if (rule) {
            var _a = rule, conditions = _a.condition, sampleRate = _a.sampleRate;
            var inner = conditions.inner;
            return {
                transaction: !inner.length ? Transaction.ALL : Transaction.MATCH_CONDITIONS,
                conditions: inner.map(function (_a) {
                    var name = _a.name, value = _a.value;
                    return ({
                        category: name,
                        match: value.join('\n'),
                    });
                }),
                sampleRate: sampleRate * 100,
                errors: {},
            };
        }
        return {
            transaction: Transaction.ALL,
            conditions: [],
            errors: {},
        };
    };
    Form.prototype.getNewCondition = function (condition) {
        var newValue = condition.match
            .split('\n')
            .filter(function (match) { return !!match.trim(); })
            .map(function (match) { return match.trim(); });
        var commonValues = {
            name: condition.category,
            value: newValue,
        };
        if (condition.category === DynamicSamplingInnerName.EVENT_RELEASE ||
            condition.category === DynamicSamplingInnerName.TRACE_RELEASE) {
            return __assign(__assign({}, commonValues), { op: DynamicSamplingInnerOperator.GLOB_MATCH });
        }
        return __assign(__assign({}, commonValues), { op: DynamicSamplingInnerOperator.EQUAL, ignoreCase: true });
    };
    Form.prototype.getSuccessMessage = function () {
        var rule = this.props.rule;
        return rule
            ? t('Successfully edited dynamic sampling rule')
            : t('Successfully added dynamic sampling rule');
    };
    Form.prototype.clearError = function (field) {
        this.setState(function (state) { return ({
            errors: omit(state.errors, field),
        }); });
    };
    Form.prototype.convertErrorXhrResponse = function (error) {
        switch (error.type) {
            case 'sampleRate':
                this.setState(function (prevState) { return ({
                    errors: __assign(__assign({}, prevState.errors), { sampleRate: error.message }),
                }); });
                break;
            default:
                addErrorMessage(error.message);
        }
    };
    Form.prototype.submitRules = function (newRules, currentRuleIndex) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, organization, project, api, onSubmitSuccess, closeModal, newProjectDetails, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project, api = _a.api, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/", { method: 'PUT', data: { dynamicSampling: { rules: newRules } } })];
                    case 2:
                        newProjectDetails = _b.sent();
                        onSubmitSuccess(newProjectDetails);
                        addSuccessMessage(this.getSuccessMessage());
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertErrorXhrResponse(handleXhrErrorResponse(error_1, currentRuleIndex));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Form.prototype.getModalTitle = function () {
        return '';
    };
    Form.prototype.geTransactionFieldDescription = function () {
        return {
            label: '',
        };
    };
    Form.prototype.getExtraFields = function () {
        return null;
    };
    Form.prototype.getCategoryOptions = function () {
        // Children have to implement this
        throw new Error('Not implemented');
    };
    Form.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal, Footer = _a.Footer;
        var _b = this.state, sampleRate = _b.sampleRate, conditions = _b.conditions, transaction = _b.transaction, errors = _b.errors;
        var transactionField = this.geTransactionFieldDescription();
        var categoryOptions = this.getCategoryOptions();
        var submitDisabled = !defined(sampleRate) ||
            (!!conditions.length &&
                !!conditions.find(function (condition) {
                    if (condition.category !== DynamicSamplingInnerName.LEGACY_BROWSERS) {
                        return !condition.match;
                    }
                    return false;
                }));
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          {this.getModalTitle()}
        </Header>
        <Body>
          <Fields>
            {this.getExtraFields()}
            <RadioField {...transactionField} name="transaction" choices={transactionChoices} onChange={function (value) { return _this.handleChange('transaction', value); }} value={transaction} inline={false} hideControlState showHelpInTooltip stacked/>
            {transaction !== Transaction.ALL && (<ConditionFields conditions={conditions} categoryOptions={categoryOptions} onAdd={this.handleAddCondition} onChange={this.handleChangeCondition} onDelete={this.handleDeleteCondition}/>)}
            <NumberField label={t('Sampling Rate')} 
        // help={t('this is a description')}  TODO(Priscila): Add correct descriptions
        name="sampleRate" onChange={function (value) {
            _this.handleChange('sampleRate', value ? Number(value) : undefined);
            if (!!errors.sampleRate) {
                _this.clearError('sampleRate');
            }
        }} placeholder={'\u0025'} value={!sampleRate ? undefined : sampleRate} inline={false} hideControlState={!errors.sampleRate} error={errors.sampleRate} showHelpInTooltip stacked/>
          </Fields>
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button onClick={closeModal}>{t('Cancel')}</Button>
            <Button priority="primary" onClick={this.handleSubmit} disabled={submitDisabled}>
              {t('Save')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return Form;
}(React.Component));
export default Form;
var Fields = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=form.jsx.map