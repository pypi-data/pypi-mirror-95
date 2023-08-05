import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { HeaderTitle } from 'app/components/charts/styles';
import ErrorBoundary from 'app/components/errorBoundary';
import { isSelectionEqual } from 'app/components/organizations/globalSelectionHeader/utils';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconDelete, IconEdit, IconGrabbable } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import WidgetCardChart from './widgetCardChart';
import WidgetQueries from './widgetQueries';
var WidgetCard = /** @class */ (function (_super) {
    __extends(WidgetCard, _super);
    function WidgetCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCard.prototype.shouldComponentUpdate = function (nextProps) {
        if (!isEqual(nextProps.widget, this.props.widget) ||
            !isSelectionEqual(nextProps.selection, this.props.selection) ||
            this.props.isEditing !== nextProps.isEditing ||
            this.props.isSorting !== nextProps.isSorting ||
            this.props.hideToolbar !== nextProps.hideToolbar) {
            return true;
        }
        return false;
    };
    WidgetCard.prototype.renderToolbar = function () {
        var _a = this.props, onEdit = _a.onEdit, onDelete = _a.onDelete, draggableProps = _a.draggableProps, hideToolbar = _a.hideToolbar, isEditing = _a.isEditing;
        if (!isEditing) {
            return null;
        }
        return (<ToolbarPanel>
        <IconContainer style={{ visibility: hideToolbar ? 'hidden' : 'visible' }}>
          <IconClick>
            <StyledIconGrabbable color="gray500" {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.listeners} {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.attributes}/>
          </IconClick>
          <IconClick data-test-id="widget-edit" onClick={function () {
            onEdit();
        }}>
            <IconEdit color="gray500"/>
          </IconClick>
          <IconClick data-test-id="widget-delete" onClick={function () {
            onDelete();
        }}>
            <IconDelete color="gray500"/>
          </IconClick>
        </IconContainer>
      </ToolbarPanel>);
    };
    WidgetCard.prototype.render = function () {
        var _this = this;
        var _a = this.props, widget = _a.widget, api = _a.api, organization = _a.organization, selection = _a.selection, renderErrorMessage = _a.renderErrorMessage, location = _a.location, router = _a.router;
        return (<ErrorBoundary customComponent={<ErrorCard>{t('Error loading widget data')}</ErrorCard>}>
        <StyledPanel isDragging={false}>
          <WidgetTitle>{widget.title}</WidgetTitle>
          <WidgetQueries api={api} organization={organization} widget={widget} selection={selection}>
            {function (_a) {
            var tableResults = _a.tableResults, timeseriesResults = _a.timeseriesResults, errorMessage = _a.errorMessage, loading = _a.loading;
            return (<React.Fragment>
                  {typeof renderErrorMessage === 'function'
                ? renderErrorMessage(errorMessage)
                : null}
                  <WidgetCardChart timeseriesResults={timeseriesResults} tableResults={tableResults} errorMessage={errorMessage} loading={loading} location={location} widget={widget} selection={selection} router={router} organization={organization}/>
                  {_this.renderToolbar()}
                </React.Fragment>);
        }}
          </WidgetQueries>
        </StyledPanel>
      </ErrorBoundary>);
    };
    return WidgetCard;
}(React.Component));
export default withApi(withOrganization(withGlobalSelection(ReactRouter.withRouter(WidgetCard))));
var ErrorCard = styled(Placeholder)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space(2));
var StyledPanel = styled(Panel, {
    shouldForwardProp: function (prop) { return prop !== 'isDragging'; },
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  overflow: hidden;\n"], ["\n  margin: 0;\n  visibility: ", ";\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  overflow: hidden;\n"])), function (p) { return (p.isDragging ? 'hidden' : 'visible'); });
var ToolbarPanel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: rgba(255, 255, 255, 0.7);\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n\n  background-color: rgba(255, 255, 255, 0.7);\n"])));
var IconContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"], ["\n  display: flex;\n  margin: 10px ", ";\n  touch-action: none;\n"])), space(2));
var IconClick = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  padding: ", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), space(1));
var StyledIconGrabbable = styled(IconGrabbable)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  &:hover {\n    cursor: grab;\n  }\n"], ["\n  &:hover {\n    cursor: grab;\n  }\n"])));
var WidgetTitle = styled(HeaderTitle)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n"], ["\n  padding: ", " ", " 0 ", ";\n  width: 100%;\n"])), space(2), space(3), space(3));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=widgetCard.jsx.map