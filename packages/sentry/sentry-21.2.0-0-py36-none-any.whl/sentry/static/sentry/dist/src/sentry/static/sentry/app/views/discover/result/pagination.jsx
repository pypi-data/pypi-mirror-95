import { __extends } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconChevron } from 'app/icons';
var Pagination = /** @class */ (function (_super) {
    __extends(Pagination, _super);
    function Pagination() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Pagination.prototype.render = function () {
        var _a = this.props, getPreviousPage = _a.getPreviousPage, getNextPage = _a.getNextPage, previous = _a.previous, next = _a.next;
        return (<ButtonBar merged>
        <Button className="btn" disabled={!previous} size="xsmall" icon={<IconChevron direction="left" size="xs"/>} onClick={getPreviousPage}/>
        <Button className="btn" disabled={!next} size="xsmall" icon={<IconChevron direction="right" size="xs"/>} onClick={getNextPage}/>
      </ButtonBar>);
    };
    return Pagination;
}(React.Component));
export default Pagination;
//# sourceMappingURL=pagination.jsx.map