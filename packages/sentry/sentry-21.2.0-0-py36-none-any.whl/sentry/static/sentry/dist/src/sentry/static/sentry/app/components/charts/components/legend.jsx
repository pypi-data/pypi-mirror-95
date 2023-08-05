import { __assign, __rest } from "tslib";
import 'echarts/lib/component/legend';
import 'echarts/lib/component/legendScroll';
import { truncationFormatter } from '../utils';
export default function Legend(props) {
    var _a = props !== null && props !== void 0 ? props : {}, truncate = _a.truncate, theme = _a.theme, textStyle = _a.textStyle, rest = __rest(_a, ["truncate", "theme", "textStyle"]);
    var formatter = function (value) { return truncationFormatter(value, truncate !== null && truncate !== void 0 ? truncate : 0); };
    var legend = __assign({ show: true, type: 'scroll', padding: 0, formatter: formatter, icon: 'circle', itemHeight: 8, itemWidth: 8, itemGap: 12, align: 'left', textStyle: __assign({ color: theme.textColor, verticalAlign: 'top', fontSize: 11, fontFamily: theme.text.family }, textStyle), inactiveColor: theme.inactive }, rest);
    return legend;
}
//# sourceMappingURL=legend.jsx.map