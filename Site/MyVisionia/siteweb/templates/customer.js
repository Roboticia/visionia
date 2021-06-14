var props = {
    decrementButton: "<strong>&minus;</strong>", // button text
    incrementButton: "<strong>&plus;</strong>", // ..
    groupClass: "", // css class of the resulting input-group
    buttonsClass: "btn-outline-secondary",
    buttonsWidth: "2.5rem",
    textAlign: "center", // alignment of the entered number
    autoDelay: 500, // ms threshold before auto value change
    autoInterval: 50, // speed of auto value change
    buttonsOnly: false, // set this `true` to disable the possibility to enter or paste the number via keyboard
    keyboardStepping: true, // set this to `false` to disallow the use of the up and down arrow keys to step
    locale: navigator.language, // the locale, per default detected automatically from the browser
    editor: I18nEditor, // the editor (parsing and rendering of the input)
    template: // the template of the input
        '<div class="input-group ${groupClass}">' +
        '<div class="input-group-prepend"><button style="min-width: ${buttonsWidth}" class="btn btn-decrement ${buttonsClass} btn-minus" type="button">${decrementButton}</button></div>' +
        '<input type="text" inputmode="decimal" style="text-align: ${textAlign}" class="form-control form-control-text-input"/>' +
        '<div class="input-group-append"><button style="min-width: ${buttonsWidth}" class="btn btn-increment ${buttonsClass} btn-plus" type="button">${incrementButton}</button></div>' +
        '</div>'
}

var RawEditor = function (props, element) {
    this.parse = function (customFormat) {
        // parse nothing
        return customFormat
    }
    this.render = function (number) {
        // render raw
        return number
    }
}