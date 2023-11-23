Object.defineProperty(MouseEvent.prototype, "detail", {
    get() {
        return opts.mouse_event.detail;
    }
});

Object.defineProperty(MouseEvent.prototype, "button", {
    get() {
        return opts.mouse_event.button;
    }
});

Object.defineProperty(MouseEvent.prototype, "buttons", {
    get() {
        return opts.mouse_event.buttons;
    }
});

