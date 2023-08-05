import { __extends } from "tslib";
import React from 'react';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
import withProjects from 'app/utils/withProjects';
var MOBILE_PLATFORMS = [
    'react-native',
    'android',
    'cordova',
    'cocoa',
    'cocoa-swift',
    'apple-ios',
    'swift',
    'flutter',
    'xamarin',
    'dotnet-xamarin',
];
var MOBILE_USER_AGENTS = ['okhttp/', 'CFNetwork/', 'Alamofire/', 'Dalvik/'];
var SuggestProjectCTA = /** @class */ (function (_super) {
    __extends(SuggestProjectCTA, _super);
    function SuggestProjectCTA() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SuggestProjectCTA.prototype.componentDidMount = function () {
        var matchedUserAgentString = this.matchedUserAgentString;
        trackAdvancedAnalyticsEvent('growth.check_show_mobile_prompt_banner', {
            matchedUserAgentString: matchedUserAgentString,
            userAgentMatches: !!matchedUserAgentString,
            hasMobileProject: this.hasMobileProject,
            snoozedOrDismissed: false,
        }, this.props.organization, { startSession: true });
    };
    Object.defineProperty(SuggestProjectCTA.prototype, "matchedUserAgentString", {
        //Returns the matched user agent string
        //otherwise, returns an empty string
        get: function () {
            var _a, _b, _c, _d;
            var entries = this.props.event.entries;
            var requestEntry = entries.find(function (item) { return item.type === 'request'; });
            if (!requestEntry) {
                return '';
            }
            var userAgent = (_c = (_b = (_a = requestEntry) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.headers) === null || _c === void 0 ? void 0 : _c.find(function (item) { return item[0].toLowerCase() === 'user-agent'; });
            if (!userAgent) {
                return '';
            }
            return ((_d = MOBILE_USER_AGENTS.find(function (mobileAgent) { var _a; return (_a = userAgent[1]) === null || _a === void 0 ? void 0 : _a.toLowerCase().includes(mobileAgent.toLowerCase()); })) !== null && _d !== void 0 ? _d : '');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "hasMobileProject", {
        //check our projects to see if there is a mobile project
        get: function () {
            return this.props.projects.some(function (project) {
                return MOBILE_PLATFORMS.includes(project.platform || '');
            });
        },
        enumerable: false,
        configurable: true
    });
    SuggestProjectCTA.prototype.render = function () {
        //TODO(Steve): implement UI
        return null;
    };
    return SuggestProjectCTA;
}(React.Component));
export default withProjects(SuggestProjectCTA);
//# sourceMappingURL=suggestProjectCTA.jsx.map