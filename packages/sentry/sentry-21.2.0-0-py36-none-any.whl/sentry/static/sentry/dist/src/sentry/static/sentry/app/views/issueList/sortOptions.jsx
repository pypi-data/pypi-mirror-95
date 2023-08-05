import React from 'react';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import { t } from 'app/locale';
import { isForReviewQuery, IssueSortOptions } from 'app/views/issueList/utils';
var IssueListSortOptions = function (_a) {
    var onSelect = _a.onSelect, sort = _a.sort, query = _a.query;
    var sortKey = sort || IssueSortOptions.DATE;
    var getSortLabel = function (key) {
        switch (key) {
            case IssueSortOptions.NEW:
                return t('First Seen');
            case IssueSortOptions.PRIORITY:
                return t('Priority');
            case IssueSortOptions.FREQ:
                return t('Events');
            case IssueSortOptions.USER:
                return t('Users');
            case IssueSortOptions.TREND:
                return t('Relative Change');
            case IssueSortOptions.INBOX:
                return t('Date Added');
            case IssueSortOptions.DATE:
            default:
                return t('Last Seen');
        }
    };
    var getMenuItem = function (key) { return (<DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      {getSortLabel(key)}
    </DropdownItem>); };
    return (<DropdownControl buttonProps={{ prefix: t('Sort by') }} label={getSortLabel(sortKey)}>
      {getMenuItem(IssueSortOptions.PRIORITY)}
      {getMenuItem(IssueSortOptions.DATE)}
      {getMenuItem(IssueSortOptions.NEW)}
      {getMenuItem(IssueSortOptions.FREQ)}
      {getMenuItem(IssueSortOptions.USER)}
      <Feature features={['issue-list-trend-sort']}>
        {getMenuItem(IssueSortOptions.TREND)}
      </Feature>
      <Feature features={['inbox']}>
        {isForReviewQuery(query) && getMenuItem(IssueSortOptions.INBOX)}
      </Feature>
    </DropdownControl>);
};
export default IssueListSortOptions;
//# sourceMappingURL=sortOptions.jsx.map