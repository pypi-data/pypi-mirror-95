export function isTransaction(event) {
    return event.type === 'transaction';
}
export function parseTraceLite(trace, event) {
    var _a, _b;
    var root = (_a = trace.find(function (e) { return e.is_root && e.event_id !== event.id; })) !== null && _a !== void 0 ? _a : null;
    var current = (_b = trace.find(function (e) { return e.event_id === event.id; })) !== null && _b !== void 0 ? _b : null;
    var children = trace.filter(function (e) { return e.parent_event_id === event.id; });
    return {
        root: root,
        current: current,
        children: children,
    };
}
//# sourceMappingURL=utils.jsx.map