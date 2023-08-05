import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
function StatusTagTooltip(_a) {
    var label = _a.label, description = _a.description, disabled = _a.disabled, children = _a.children;
    return (<Tooltip title={<Title>
          <Label>{label}</Label>
          {description && <div>{description}</div>}
        </Title>} disabled={disabled}>
      {children}
    </Tooltip>);
}
export default StatusTagTooltip;
var Title = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  margin-bottom: ", ";\n"], ["\n  display: inline-block;\n  margin-bottom: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=statusTooltip.jsx.map