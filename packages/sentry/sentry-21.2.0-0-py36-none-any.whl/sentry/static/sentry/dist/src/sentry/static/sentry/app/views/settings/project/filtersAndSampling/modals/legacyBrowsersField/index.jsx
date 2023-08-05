import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import BulkController from 'app/components/bulkController';
import { PanelTable } from 'app/components/panels';
import Switch from 'app/components/switchButton';
import { LEGACY_BROWSER_LIST } from '../utils';
import LegacyBrowser from './legacyBrowser';
var legacyBrowsers = Object.keys(LEGACY_BROWSER_LIST);
function LegacyBrowsersField(_a) {
    var onChange = _a.onChange;
    function handleChange(_a) {
        var selectedIds = _a.selectedIds;
        onChange(selectedIds);
    }
    return (<BulkController pageIds={legacyBrowsers} allRowsCount={legacyBrowsers.length} onChange={handleChange} columnsCount={0}>
      {function (_a) {
        var selectedIds = _a.selectedIds, onRowToggle = _a.onRowToggle, onAllRowsToggle = _a.onAllRowsToggle, isAllSelected = _a.isAllSelected;
        return (<StyledPanelTable headers={[
            '',
            <Switch key="switch" size="lg" isActive={isAllSelected} toggle={function () {
                onAllRowsToggle(!isAllSelected);
            }}/>,
        ]}>
          {legacyBrowsers.map(function (legacyBrowser) { return (<LegacyBrowser key={legacyBrowser} browser={legacyBrowser} isEnabled={selectedIds.includes(legacyBrowser)} onToggle={function () {
            onRowToggle(legacyBrowser);
        }}/>); })}
        </StyledPanelTable>);
    }}
    </BulkController>);
}
export default LegacyBrowsersField;
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"], ["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map