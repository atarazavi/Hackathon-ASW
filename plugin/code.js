"use strict";
// Design Review AI - Main plugin code (sandbox)
figma.showUI(__html__, { width: 400, height: 300 });
figma.ui.onmessage = async (msg) => {
    if (msg.type === 'get-selection') {
        const selection = figma.currentPage.selection;
        if (selection.length === 0) {
            figma.ui.postMessage({ type: 'error', message: 'No frames selected. Please select one or more frames.' });
            return;
        }
        // Extract basic info from selection (Phase 2B will expand this)
        const data = selection.map(node => ({
            name: node.name,
            type: node.type,
            width: 'width' in node ? node.width : 0,
            height: 'height' in node ? node.height : 0,
        }));
        figma.ui.postMessage({ type: 'selection-data', data });
    }
    if (msg.type === 'close') {
        figma.closePlugin();
    }
};
