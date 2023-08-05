import { __values } from "tslib";
import plugins from 'app/plugins';
var CONTEXT_TYPES = {
    default: require('app/components/events/contexts/default').default,
    app: require('app/components/events/contexts/app/app').default,
    device: require('app/components/events/contexts/device/device').default,
    os: require('app/components/events/contexts/operatingSystem/operatingSystem').default,
    runtime: require('app/components/events/contexts/runtime/runtime').default,
    user: require('app/components/events/contexts/user/user').default,
    gpu: require('app/components/events/contexts/gpu/gpu').default,
    trace: require('app/components/events/contexts/trace/trace').default,
    // 'redux.state' will be replaced with more generic context called 'state'
    'redux.state': require('app/components/events/contexts/redux').default,
    state: require('app/components/events/contexts/state').default,
};
export function getContextComponent(type) {
    return CONTEXT_TYPES[type] || plugins.contexts[type] || CONTEXT_TYPES.default;
}
export function getSourcePlugin(pluginContexts, contextType) {
    var e_1, _a;
    if (CONTEXT_TYPES[contextType]) {
        return null;
    }
    try {
        for (var pluginContexts_1 = __values(pluginContexts), pluginContexts_1_1 = pluginContexts_1.next(); !pluginContexts_1_1.done; pluginContexts_1_1 = pluginContexts_1.next()) {
            var plugin = pluginContexts_1_1.value;
            if (plugin.contexts.indexOf(contextType) >= 0) {
                return plugin;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (pluginContexts_1_1 && !pluginContexts_1_1.done && (_a = pluginContexts_1.return)) _a.call(pluginContexts_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return null;
}
//# sourceMappingURL=utils.jsx.map