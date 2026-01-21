"use strict";
// Design Review AI - Main plugin code (sandbox)
figma.showUI(__html__, { width: 400, height: 500 });
// Helper: Convert Figma RGB (0-1) to hex
function rgbToHex(color) {
    const r = Math.round(color.r * 255);
    const g = Math.round(color.g * 255);
    const b = Math.round(color.b * 255);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}
// Extract a single layer with all its properties
function extractLayer(node, depth = 0) {
    // Limit recursion depth to prevent stack overflow (max 15)
    if (depth > 15)
        return null;
    // Skip invisible layers to reduce payload
    if ('visible' in node && !node.visible)
        return null;
    const layer = {
        id: node.id,
        name: node.name,
        type: node.type,
        visible: 'visible' in node ? node.visible : true,
        x: 'x' in node ? node.x : 0,
        y: 'y' in node ? node.y : 0,
        width: 'width' in node ? node.width : 0,
        height: 'height' in node ? node.height : 0,
        opacity: 'opacity' in node ? node.opacity : 1,
        fills: [],
        strokes: [],
        children: [],
    };
    // Extract fills (solid colors only for simplicity)
    if ('fills' in node && node.fills !== figma.mixed && Array.isArray(node.fills)) {
        layer.fills = node.fills
            .filter((fill) => fill.type === 'SOLID' && fill.visible !== false)
            .map(fill => {
            var _a;
            return ({
                type: 'SOLID',
                color: rgbToHex(fill.color),
                opacity: (_a = fill.opacity) !== null && _a !== void 0 ? _a : 1,
            });
        });
    }
    // Extract strokes
    if ('strokes' in node && Array.isArray(node.strokes)) {
        const strokeWeight = 'strokeWeight' in node ?
            (node.strokeWeight === figma.mixed ? 1 : node.strokeWeight) : 0;
        layer.strokes = node.strokes
            .filter((stroke) => stroke.type === 'SOLID' && stroke.visible !== false)
            .map(stroke => ({
            type: 'SOLID',
            color: rgbToHex(stroke.color),
            weight: strokeWeight,
        }));
    }
    // Extract text properties
    if (node.type === 'TEXT') {
        const textNode = node;
        layer.text = {
            content: textNode.characters,
            fontSize: textNode.fontSize === figma.mixed ? 'mixed' : textNode.fontSize,
            fontFamily: textNode.fontName === figma.mixed ? 'mixed' : textNode.fontName.family,
            fontStyle: textNode.fontName === figma.mixed ? 'mixed' : textNode.fontName.style,
        };
        // Get text fill color (first solid fill)
        if (textNode.fills !== figma.mixed && Array.isArray(textNode.fills)) {
            const solidFill = textNode.fills.find((f) => f.type === 'SOLID');
            if (solidFill) {
                layer.text.fillColor = rgbToHex(solidFill.color);
            }
        }
    }
    // Recursively extract children
    if ('children' in node) {
        layer.children = node.children
            .map(child => extractLayer(child, depth + 1))
            .filter((child) => child !== null);
    }
    return layer;
}
// Extract a complete frame
function extractFrame(node) {
    const layers = extractLayer(node);
    return {
        id: node.id,
        name: node.name,
        width: 'width' in node ? node.width : 0,
        height: 'height' in node ? node.height : 0,
        layers: layers ? [layers] : [],
    };
}
figma.ui.onmessage = async (msg) => {
    var _a, _b;
    if (msg.type === 'get-selection') {
        const selection = figma.currentPage.selection;
        if (selection.length === 0) {
            figma.ui.postMessage({
                type: 'error',
                message: 'No frames selected. Please select one or more frames.'
            });
            return;
        }
        // Filter to only frames/components/instances (not individual shapes)
        const frameNodes = selection.filter(node => node.type === 'FRAME' || node.type === 'COMPONENT' || node.type === 'INSTANCE');
        if (frameNodes.length === 0) {
            figma.ui.postMessage({
                type: 'error',
                message: 'Please select frames, components, or instances (not individual shapes).'
            });
            return;
        }
        // Extract design data from all selected frames
        const frames = frameNodes.map(extractFrame);
        figma.ui.postMessage({
            type: 'design-data',
            data: { frames }
        });
    }
    if (msg.type === 'analysis-complete') {
        const findingCount = (_b = (_a = msg.data) === null || _a === void 0 ? void 0 : _a.findingCount) !== null && _b !== void 0 ? _b : 0;
        figma.notify(`Analysis complete: ${findingCount} finding(s)`);
    }
    if (msg.type === 'close') {
        figma.closePlugin();
    }
};
