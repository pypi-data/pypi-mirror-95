import { __assign, __awaiter, __generator, __read, __rest, __spread } from "tslib";
import { browserHistory } from 'react-router';
import { Severity } from '@sentry/react';
import jQuery from 'jquery';
import Cookies from 'js-cookie';
import isUndefined from 'lodash/isUndefined';
import { openSudo, redirectToProject } from 'app/actionCreators/modal';
import { PROJECT_MOVED, SUDO_REQUIRED, SUPERUSER_REQUIRED, } from 'app/constants/apiErrorCodes';
import ajaxCsrfSetup from 'app/utils/ajaxCsrfSetup';
import { metric } from 'app/utils/analytics';
import { run } from 'app/utils/apiSentryClient';
import { uniqueId } from 'app/utils/guid';
import createRequestError from 'app/utils/requestError/createRequestError';
import { EXPERIMENTAL_SPA } from './constants';
var Request = /** @class */ (function () {
    function Request(xhr) {
        this.xhr = xhr;
        this.alive = true;
    }
    Request.prototype.cancel = function () {
        this.alive = false;
        this.xhr.abort();
        metric('app.api.request-abort', 1);
    };
    return Request;
}());
export { Request };
/**
 * Setup the CSRF + other client early initalization.
 */
export function initApiClient() {
    jQuery.ajaxSetup({
        // jQuery won't allow using the ajaxCsrfSetup function directly
        beforeSend: ajaxCsrfSetup,
        // Completely disable evaluation of script responses using jQuery ajax
        // Typically the `text script` converter will eval the text [1]. Instead we
        // just immediately return.
        // [1]: https://github.com/jquery/jquery/blob/8969732518470a7f8e654d5bc5be0b0076cb0b87/src/ajax/script.js#L39-L42
        converters: {
            'text script': function (value) { return value; },
        },
    });
}
// TODO: Need better way of identifying anonymous pages that don't trigger redirect
var ALLOWED_ANON_PAGES = [
    /^\/accept\//,
    /^\/share\//,
    /^\/auth\/login\//,
    /^\/join-request\//,
];
export function initApiClientErrorHandling() {
    jQuery(document).ajaxError(function (_evt, jqXHR) {
        var _a, _b, _c, _d;
        var pageAllowsAnon = ALLOWED_ANON_PAGES.find(function (regex) {
            return regex.test(window.location.pathname);
        });
        // Ignore error unless it is a 401
        if (!jqXHR || jqXHR.status !== 401 || pageAllowsAnon) {
            return;
        }
        var code = (_b = (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
        var extra = (_d = (_c = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra;
        // 401s can also mean sudo is required or it's a request that is allowed to fail
        // Ignore if these are the cases
        if (code === 'sudo-required' || code === 'ignore') {
            return;
        }
        // If user must login via SSO, redirect to org login page
        if (code === 'sso-required') {
            window.location.assign(extra.loginUrl);
            return;
        }
        // Otherwise, the user has become unauthenticated. Send them to auth
        Cookies.set('session_expired', '1');
        if (EXPERIMENTAL_SPA) {
            browserHistory.replace('/auth/login/');
        }
        else {
            window.location.reload();
        }
    });
}
/**
 * Construct a full request URL
 */
function buildRequestUrl(baseUrl, path, query) {
    var params;
    try {
        params = jQuery.param(query !== null && query !== void 0 ? query : [], true);
    }
    catch (err) {
        run(function (Sentry) {
            return Sentry.withScope(function (scope) {
                scope.setExtra('path', path);
                scope.setExtra('query', query);
                Sentry.captureException(err);
            });
        });
        throw err;
    }
    var fullUrl;
    // Append the baseUrl
    if (path.indexOf(baseUrl) === -1) {
        fullUrl = baseUrl + path;
    }
    else {
        fullUrl = path;
    }
    if (!params) {
        return fullUrl;
    }
    // Append query parameters
    if (fullUrl.indexOf('?') !== -1) {
        fullUrl += '&' + params;
    }
    else {
        fullUrl += '?' + params;
    }
    return fullUrl;
}
/**
 * Check if the API response says project has been renamed.  If so, redirect
 * user to new project slug
 */
// TODO(ts): refine this type later
export function hasProjectBeenRenamed(response) {
    var _a, _b, _c, _d, _e;
    var code = (_b = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === null || _b === void 0 ? void 0 : _b.code;
    // XXX(billy): This actually will never happen because we can't intercept the 302
    // jQuery ajax will follow the redirect by default...
    if (code !== PROJECT_MOVED) {
        return false;
    }
    var slug = (_e = (_d = (_c = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.extra) === null || _e === void 0 ? void 0 : _e.slug;
    redirectToProject(slug);
    return true;
}
/**
 * The API client is used to make HTTP requests to Sentry's backend.
 *
 * This is the prefered way to talk to the backend.
 */
var Client = /** @class */ (function () {
    function Client(options) {
        if (options === void 0) { options = {}; }
        var _a;
        this.baseUrl = (_a = options.baseUrl) !== null && _a !== void 0 ? _a : '/api/0';
        this.activeRequests = {};
    }
    Client.prototype.wrapCallback = function (id, func, cleanup) {
        var _this = this;
        if (cleanup === void 0) { cleanup = false; }
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var req = _this.activeRequests[id];
            if (cleanup === true) {
                delete _this.activeRequests[id];
            }
            if (req && req.alive) {
                // Check if API response is a 302 -- means project slug was renamed and user
                // needs to be redirected
                // @ts-expect-error
                if (hasProjectBeenRenamed.apply(void 0, __spread(args))) {
                    return;
                }
                if (isUndefined(func)) {
                    return;
                }
                // Call success callback
                return func.apply(req, args); // eslint-disable-line
            }
        };
    };
    /**
     * Attempt to cancel all active XHR requests
     */
    Client.prototype.clear = function () {
        Object.values(this.activeRequests).forEach(function (r) { return r.cancel(); });
    };
    Client.prototype.handleRequestError = function (_a, response, textStatus, errorThrown) {
        var _this = this;
        var _b, _c;
        var id = _a.id, path = _a.path, requestOptions = _a.requestOptions;
        var code = (_c = (_b = response === null || response === void 0 ? void 0 : response.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) === null || _c === void 0 ? void 0 : _c.code;
        var isSudoRequired = code === SUDO_REQUIRED || code === SUPERUSER_REQUIRED;
        if (isSudoRequired) {
            openSudo({
                superuser: code === SUPERUSER_REQUIRED,
                sudo: code === SUDO_REQUIRED,
                retryRequest: function () { return __awaiter(_this, void 0, void 0, function () {
                    var data, err_1;
                    var _a, _b;
                    return __generator(this, function (_c) {
                        switch (_c.label) {
                            case 0:
                                _c.trys.push([0, 2, , 3]);
                                return [4 /*yield*/, this.requestPromise(path, requestOptions)];
                            case 1:
                                data = _c.sent();
                                (_a = requestOptions.success) === null || _a === void 0 ? void 0 : _a.call(requestOptions, data);
                                return [3 /*break*/, 3];
                            case 2:
                                err_1 = _c.sent();
                                (_b = requestOptions.error) === null || _b === void 0 ? void 0 : _b.call(requestOptions, err_1);
                                return [3 /*break*/, 3];
                            case 3: return [2 /*return*/];
                        }
                    });
                }); },
                onClose: function () { var _a; return (_a = 
                // If modal was closed, then forward the original response
                requestOptions.error) === null || _a === void 0 ? void 0 : _a.call(
                // If modal was closed, then forward the original response
                requestOptions, response); },
            });
            return;
        }
        // Call normal error callback
        var errorCb = this.wrapCallback(id, requestOptions.error);
        errorCb === null || errorCb === void 0 ? void 0 : errorCb(response, textStatus, errorThrown);
    };
    /**
     * Initate a request to the backend API.
     *
     * Consider using `requestPromise` for the async Promise version of this method.
     */
    Client.prototype.request = function (path, options) {
        var _this = this;
        if (options === void 0) { options = {}; }
        var method = options.method || (options.data ? 'POST' : 'GET');
        var data = options.data;
        if (!isUndefined(data) && method !== 'GET') {
            data = JSON.stringify(data);
        }
        var fullUrl = buildRequestUrl(this.baseUrl, path, options.query);
        var id = uniqueId();
        var startMarker = "api-request-start-" + id;
        metric.mark({ name: startMarker });
        var errorObject = new Error();
        /**
         * Called when the request completes with a 2xx status
         */
        var successHandler = function (responseData, textStatus, xhr) {
            metric.measure({
                name: 'app.api.request-success',
                start: startMarker,
                data: { status: xhr === null || xhr === void 0 ? void 0 : xhr.status },
            });
            if (!isUndefined(options.success)) {
                _this.wrapCallback(id, options.success)(responseData, textStatus, xhr);
            }
        };
        /**
         * Called when the request is non-2xx
         */
        var errorHandler = function (resp, textStatus, errorThrown) {
            metric.measure({
                name: 'app.api.request-error',
                start: startMarker,
                data: { status: resp === null || resp === void 0 ? void 0 : resp.status },
            });
            if (resp && resp.status !== 0 && resp.status !== 404) {
                run(function (Sentry) {
                    return Sentry.withScope(function (scope) {
                        var _a;
                        // `requestPromise` can pass its error object
                        var preservedError = (_a = options.preservedError) !== null && _a !== void 0 ? _a : errorObject;
                        var errorObjectToUse = createRequestError(resp, preservedError.stack, method, path);
                        errorObjectToUse.removeFrames(3);
                        // Setting this to warning because we are going to capture all failed requests
                        scope.setLevel(Severity.Warning);
                        scope.setTag('http.statusCode', String(resp.status));
                        Sentry.captureException(errorObjectToUse);
                    });
                });
            }
            _this.handleRequestError({ id: id, path: path, requestOptions: options }, resp, textStatus, errorThrown);
        };
        /**
         * Called when the request completes
         */
        var completeHandler = function (jqXHR, textStatus) {
            return _this.wrapCallback(id, options.complete, true)(jqXHR, textStatus);
        };
        var xhrRequest = jQuery.ajax({
            url: fullUrl,
            method: method,
            data: data,
            contentType: 'application/json',
            headers: {
                Accept: 'application/json; charset=utf-8',
            },
            success: successHandler,
            error: errorHandler,
            complete: completeHandler,
        });
        var request = new Request(xhrRequest);
        this.activeRequests[id] = request;
        return request;
    };
    Client.prototype.requestPromise = function (path, _a) {
        var _this = this;
        if (_a === void 0) { _a = {}; }
        var includeAllArgs = _a.includeAllArgs, options = __rest(_a, ["includeAllArgs"]);
        // Create an error object here before we make any async calls so
        // that we have a helpful stack trace if it errors
        //
        // This *should* get logged to Sentry only if the promise rejection is not handled
        // (since SDK captures unhandled rejections). Ideally we explicitly ignore rejection
        // or handle with a user friendly error message
        var preservedError = new Error();
        return new Promise(function (resolve, reject) {
            _this.request(path, __assign(__assign({}, options), { preservedError: preservedError, success: function (data, textStatus, xhr) {
                    includeAllArgs ? resolve([data, textStatus, xhr]) : resolve(data);
                }, error: function (resp) {
                    var errorObjectToUse = createRequestError(resp, preservedError.stack, options.method, path);
                    errorObjectToUse.removeFrames(2);
                    // Although `this.request` logs all error responses, this error object can
                    // potentially be logged by Sentry's unhandled rejection handler
                    reject(errorObjectToUse);
                } }));
        });
    };
    return Client;
}());
export { Client };
//# sourceMappingURL=api.jsx.map