export var DynamicSamplingRuleType;
(function (DynamicSamplingRuleType) {
    /**
     * The rule applies to traces (transaction events considered in the context of a trace)
     */
    DynamicSamplingRuleType["TRACE"] = "trace";
    /**
     *  The rule applies to transaction events considered independently
     */
    DynamicSamplingRuleType["TRANSACTION"] = "transaction";
    /**
     * The rule applies to error events (not transaction events)
     */
    DynamicSamplingRuleType["ERROR"] = "error";
})(DynamicSamplingRuleType || (DynamicSamplingRuleType = {}));
export var DynamicSamplingConditionOperator;
(function (DynamicSamplingConditionOperator) {
    /**
     * The not combinator has a similar structure with the only difference that "inner" is not an array
     * and contains directly the negated condition
     */
    DynamicSamplingConditionOperator["NOT"] = "not";
    /**
     * Combine multiple sub-conditions with the operator 'or'
     */
    DynamicSamplingConditionOperator["OR"] = "or";
    /**
     * Combine multiple sub-conditions with the operator 'and'
     */
    DynamicSamplingConditionOperator["AND"] = "and";
})(DynamicSamplingConditionOperator || (DynamicSamplingConditionOperator = {}));
export var DynamicSamplingInnerOperator;
(function (DynamicSamplingInnerOperator) {
    /**
     * It uses glob matches for checking (e.g. releases use glob matching "1.1.*" will match release 1.1.1 and 1.1.2)
     */
    DynamicSamplingInnerOperator["GLOB_MATCH"] = "glob";
    /**
     * It uses simple equality for checking
     */
    DynamicSamplingInnerOperator["EQUAL"] = "eq";
})(DynamicSamplingInnerOperator || (DynamicSamplingInnerOperator = {}));
export var DynamicSamplingInnerName;
(function (DynamicSamplingInnerName) {
    DynamicSamplingInnerName["TRACE_RELEASE"] = "trace.release";
    DynamicSamplingInnerName["TRACE_ENVIRONMENT"] = "trace.environment";
    DynamicSamplingInnerName["TRACE_USER"] = "trace.user";
    DynamicSamplingInnerName["EVENT_RELEASE"] = "event.release";
    DynamicSamplingInnerName["EVENT_ENVIRONMENT"] = "event.environment";
    DynamicSamplingInnerName["EVENT_USER"] = "event.user";
    DynamicSamplingInnerName["LEGACY_BROWSERS"] = "legacy-browsers";
})(DynamicSamplingInnerName || (DynamicSamplingInnerName = {}));
//# sourceMappingURL=dynamicSampling.jsx.map