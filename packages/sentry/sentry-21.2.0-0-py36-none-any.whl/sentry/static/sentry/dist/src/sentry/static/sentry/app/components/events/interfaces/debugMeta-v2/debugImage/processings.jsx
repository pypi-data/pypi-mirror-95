import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import ProcessingItem from '../processing/item';
import ProcessingList from '../processing/list';
import ProcessingIcon from './processingIcon';
function Processings(_a) {
    var unwind_status = _a.unwind_status, debug_status = _a.debug_status;
    var items = [];
    if (debug_status) {
        items.push(<ProcessingItem key="symbolication" type="symbolication" icon={<ProcessingIcon status={debug_status}/>}/>);
    }
    if (unwind_status) {
        items.push(<ProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<ProcessingIcon status={unwind_status}/>}/>);
    }
    return <StyledProcessingList items={items}/>;
}
export default Processings;
var StyledProcessingList = styled(ProcessingList)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-auto-flow: row;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-auto-flow: column;\n    grid-gap: ", ";\n  }\n"], ["\n  grid-auto-flow: row;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-auto-flow: column;\n    grid-gap: ", ";\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[3]; }, space(1.5));
var templateObject_1;
//# sourceMappingURL=processings.jsx.map