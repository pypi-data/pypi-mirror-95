import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 30%;\n      margin-left: -15%;\n    }\n  }\n"], ["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 30%;\n      margin-left: -15%;\n    }\n  }\n"])), theme.breakpoints[0], theme.breakpoints[1], theme.breakpoints[4]);
export var LEGACY_BROWSER_LIST = {
    ie_pre_9: {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 8 and lower'),
    },
    ie9: {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 9'),
    },
    ie10: {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 10'),
    },
    ie11: {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 11'),
    },
    safari_pre_6: {
        icon: 'safari',
        title: t('Safari Version 5 and lower'),
    },
    opera_pre_15: {
        icon: 'opera',
        title: t('Opera Version 14 and lower'),
    },
    opera_mini_pre_8: {
        icon: 'opera',
        title: t('Opera Mini Version 8 and lower'),
    },
    android_pre_4: {
        icon: 'android',
        title: t('Android Version 3 and lower'),
    },
};
export var Transaction;
(function (Transaction) {
    Transaction["ALL"] = "all";
    Transaction["MATCH_CONDITIONS"] = "match-conditions";
})(Transaction || (Transaction = {}));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map