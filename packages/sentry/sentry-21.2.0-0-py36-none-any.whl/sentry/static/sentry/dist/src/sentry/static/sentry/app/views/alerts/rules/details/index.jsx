import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { fetchOrgMembers } from 'app/actionCreators/members';
import Feature from 'app/components/acl/feature';
import withApi from 'app/utils/withApi';
import { fetchAlertRule, fetchIncidentsForRule } from '../../utils';
import DetailsBody from './body';
import DetailsHeader from './header';
var AlertRuleDetails = /** @class */ (function (_super) {
    __extends(AlertRuleDetails, _super);
    function AlertRuleDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, ruleId, rulePromise, incidentsPromise, _err_1;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ isLoading: true, hasError: false });
                        _a = this.props.params, orgId = _a.orgId, ruleId = _a.ruleId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        rulePromise = fetchAlertRule(orgId, ruleId).then(function (rule) {
                            return _this.setState({ rule: rule });
                        });
                        incidentsPromise = fetchIncidentsForRule(orgId, ruleId).then(function (incidents) {
                            return _this.setState({ incidents: incidents });
                        });
                        return [4 /*yield*/, Promise.all([rulePromise, incidentsPromise])];
                    case 2:
                        _b.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRuleDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, params = _a.params;
        fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    AlertRuleDetails.prototype.render = function () {
        var _a = this.state, rule = _a.rule, incidents = _a.incidents, hasError = _a.hasError;
        var _b = this.props, params = _b.params, organization = _b.organization;
        return (<React.Fragment>
        <Feature organization={organization} features={['alert-details-redesign']}>
          <DetailsHeader hasIncidentRuleDetailsError={hasError} params={params} rule={rule}/>
          <DetailsBody {...this.props} rule={rule} incidents={incidents}/>
        </Feature>
      </React.Fragment>);
    };
    return AlertRuleDetails;
}(React.Component));
export default withApi(AlertRuleDetails);
//# sourceMappingURL=index.jsx.map