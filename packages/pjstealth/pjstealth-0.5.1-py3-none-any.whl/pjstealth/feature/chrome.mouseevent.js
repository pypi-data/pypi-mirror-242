Object.defineProperty(MouseEvent.prototype, "detail", {
    get() {
        if (this.type === 'mousedown') {
            return opts.mouse_event.detail;
        } else {
            console.log("no")
        }
    }
});

// Object.defineProperty(MouseEvent.prototype, "button", {
//     get() {
//         return opts.mouse_event.button;
//     }
// });
//
// Object.defineProperty(MouseEvent.prototype, "buttons", {
//     get() {
//         return opts.mouse_event.buttons;
//     }
// });

