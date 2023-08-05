import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconFire, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { formattedValue } from 'app/utils/measurements/index';
import { LONG_WEB_VITAL_NAMES, WEB_VITAL_DETAILS, } from 'app/views/performance/transactionVitals/constants';
function isOutdatedSdk(event) {
    var _a;
    if (!((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.version)) {
        return false;
    }
    var sdkVersion = event.sdk.version;
    return (sdkVersion.startsWith('5.26.') ||
        sdkVersion.startsWith('5.27.0') ||
        sdkVersion.startsWith('5.27.1') ||
        sdkVersion.startsWith('5.27.2'));
}
export default function EventVitals(_a) {
    var _b;
    var event = _a.event, _c = _a.showSectionHeader, showSectionHeader = _c === void 0 ? true : _c;
    var measurementNames = Object.keys((_b = event.measurements) !== null && _b !== void 0 ? _b : {})
        .filter(function (name) {
        // ignore marker measurements
        return !name.startsWith('mark.');
    })
        .sort();
    if (measurementNames.length === 0) {
        return null;
    }
    var component = (<Measurements>
      {measurementNames.map(function (name) { return (<EventVital key={name} event={event} name={name}/>); })}
    </Measurements>);
    if (showSectionHeader) {
        return (<Container>
        <SectionHeading>
          {t('Web Vitals')}
          {isOutdatedSdk(event) && (<WarningIconContainer size="sm">
              <Tooltip title={t('These vitals were collected using an outdated SDK version and may not be accurate. To ensure accurate web vitals in new transaction events, please update your SDK to the latest version.')} position="top" containerDisplayMode="inline-block">
                <IconWarning size="sm"/>
              </Tooltip>
            </WarningIconContainer>)}
        </SectionHeading>
        {component}
      </Container>);
    }
    return component;
}
function EventVital(_a) {
    var _b, _c, _d, _e;
    var event = _a.event, name = _a.name;
    var value = (_c = (_b = event.measurements) === null || _b === void 0 ? void 0 : _b[name].value) !== null && _c !== void 0 ? _c : null;
    if (value === null) {
        return null;
    }
    var record = Object.values(WEB_VITAL_DETAILS).find(function (vital) { return vital.slug === name; });
    var failedThreshold = record ? value >= record.failureThreshold : false;
    var currentValue = formattedValue(record, value);
    var thresholdValue = formattedValue(record, (_d = record === null || record === void 0 ? void 0 : record.failureThreshold) !== null && _d !== void 0 ? _d : 0);
    if (!LONG_WEB_VITAL_NAMES.hasOwnProperty(name)) {
        return null;
    }
    return (<EventVitalContainer>
      <StyledPanel failedThreshold={failedThreshold}>
        <Name>{(_e = LONG_WEB_VITAL_NAMES[name]) !== null && _e !== void 0 ? _e : name}</Name>
        <ValueRow>
          {failedThreshold ? (<FireIconContainer size="sm">
              <Tooltip title={t('Fails threshold at %s.', thresholdValue)} position="top" containerDisplayMode="inline-block">
                <IconFire size="sm"/>
              </Tooltip>
            </FireIconContainer>) : null}
          <Value failedThreshold={failedThreshold}>{currentValue}</Value>
        </ValueRow>
      </StyledPanel>
    </EventVitalContainer>);
}
var Measurements = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n"])), space(1));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(4));
var StyledPanel = styled(Panel)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"], ["\n  padding: ", " ", ";\n  margin-bottom: ", ";\n  ", "\n"])), space(1), space(1.5), space(1), function (p) { return p.failedThreshold && "border: 1px solid " + p.theme.red300 + ";"; });
var Name = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var ValueRow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var WarningIconContainer = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-left: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space(0.5), function (p) { return p.theme.red300; });
var FireIconContainer = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n  margin-right: ", ";\n  color: ", ";\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, space(0.5), function (p) { return p.theme.red300; });
var Value = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return p.failedThreshold && "color: " + p.theme.red300 + ";"; });
export var EventVitalContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=eventVitals.jsx.map