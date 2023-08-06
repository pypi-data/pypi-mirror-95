export let RenderWindowInteractor;
const vtk = window.vtk;
if (vtk) {
    const macro = vtk.macro;
    const vtkRenderWindowInteractor = vtk.Rendering.Core.vtkRenderWindowInteractor;
    // ----------------------------------------------------------------------------
    // panelRenderWindowInteractor fix findPokeRenderer
    // ----------------------------------------------------------------------------
    function panelRenderWindowInteractor(publicAPI, model) {
        // Set our className
        model.classHierarchy.push("panelRenderWindowInteractor");
        publicAPI.findPokedRenderer = (x = 0, y = 0) => {
            if (!model.view) {
                return null;
            }
            const rc = model.view.getRenderable().getRenderersByReference();
            rc.sort((a, b) => a.getLayer() - b.getLayer());
            let interactiveren = null;
            let viewportren = null;
            let currentRenderer = null;
            let count = rc.length;
            while (count--) {
                const aren = rc[count];
                if (model.view.isInViewport(x, y, aren) && aren.getInteractive()) {
                    currentRenderer = aren;
                    break;
                }
                if (interactiveren === null && aren.getInteractive()) {
                    // Save this renderer in case we can't find one in the viewport that
                    // is interactive.
                    interactiveren = aren;
                }
                if (viewportren === null && model.view.isInViewport(x, y, aren)) {
                    // Save this renderer in case we can't find one in the viewport that
                    // is interactive.
                    viewportren = aren;
                }
            }
            // We must have a value.  If we found an interactive renderer before, that's
            // better than a non-interactive renderer.
            if (currentRenderer === null) {
                currentRenderer = interactiveren;
            }
            // We must have a value.  If we found a renderer that is in the viewport,
            // that is better than any old viewport (but not as good as an interactive
            // one).
            if (currentRenderer === null) {
                currentRenderer = viewportren;
            }
            // We must have a value - take anything.
            if (currentRenderer == null) {
                currentRenderer = rc[0];
            }
            return currentRenderer;
        };
    }
    // ----------------------------------------------------------------------------
    // Object factory
    // ----------------------------------------------------------------------------
    RenderWindowInteractor = {
        newInstance: macro.newInstance((publicAPI, model, initialValues = {}) => {
            vtkRenderWindowInteractor.extend(publicAPI, model, initialValues);
            // Object specific methods
            panelRenderWindowInteractor(publicAPI, model);
        }, "panelRenderWindowInteractor"),
    };
}
//# sourceMappingURL=vtkrenderwindowinteractor.js.map