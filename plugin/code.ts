// Design Review AI - Main plugin code (sandbox)
figma.showUI(__html__, { width: 400, height: 300 });

// Type definitions for extracted design data
interface ExtractedFrame {
  id: string;
  name: string;
  width: number;
  height: number;
  layers: ExtractedLayer[];
}

interface ExtractedLayer {
  id: string;
  name: string;
  type: string;
  visible: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
  opacity: number;
  fills: ExtractedFill[];
  strokes: ExtractedStroke[];
  children: ExtractedLayer[];
  text?: ExtractedText;
}

interface ExtractedFill {
  type: string;
  color?: string;  // hex format #RRGGBB
  opacity: number;
}

interface ExtractedStroke {
  type: string;
  color?: string;
  weight: number;
}

interface ExtractedText {
  content: string;
  fontSize: number | 'mixed';
  fontFamily: string | 'mixed';
  fontStyle: string | 'mixed';
  fillColor?: string;
}

figma.ui.onmessage = async (msg: { type: string; data?: any }) => {
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
