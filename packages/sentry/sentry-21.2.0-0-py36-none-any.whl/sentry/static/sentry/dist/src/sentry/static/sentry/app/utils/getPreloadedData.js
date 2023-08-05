export function getPreloadedDataPromise(name, slug, fallback, isInitialFetch) {
    var data = window.__sentry_preload;
    if (!isInitialFetch ||
        !data ||
        data.orgSlug.toLowerCase() !== slug.toLowerCase() ||
        !data[name].then) {
        return fallback();
    }
    return data[name].catch(fallback);
}
//# sourceMappingURL=getPreloadedData.js.map