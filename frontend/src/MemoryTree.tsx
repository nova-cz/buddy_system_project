
import { motion } from "framer-motion";
import React from "react";
export interface MemoryNode {
    size: number;
    size_str?: string;
    is_free: boolean;
    process: string | null;
    left: MemoryNode | null;
    right: MemoryNode | null;
}

interface PositionedNode extends MemoryNode {
    x: number;
    y: number;
    id: string;
    parentId?: string;
}

interface MemoryTreeProps {
    node: MemoryNode;
}

const blockColors = {
    free: "#b2f7b8",
    occupied: "#f7b2b2",
};


// Responsive layout: calcula posiciones relativas (0-1) y escala según el ancho real
function layoutTreeResponsive(root: MemoryNode, levelHeight = 80) {
    let nodes: (PositionedNode & { relX: number })[] = [];
    let maxDepth = 0;
    function traverse(node: MemoryNode, depth: number, relX: number, parentId?: string, id = "0") {
        if (!node) return;
        maxDepth = Math.max(maxDepth, depth);
        nodes.push({ ...node, x: 0, y: depth * levelHeight, relX, id, parentId });
        if (node.left && node.right) {
            traverse(node.left, depth + 1, relX - 1 / Math.pow(2, depth + 2), id, id + "L");
            traverse(node.right, depth + 1, relX + 1 / Math.pow(2, depth + 2), id, id + "R");
        }
    }
    traverse(root, 0, 0.5);
    return { nodes, maxDepth };
}


const MemoryTree: React.FC<MemoryTreeProps> = ({ node }) => {
    const containerRef = React.useRef<HTMLDivElement>(null);
    const [containerWidth, setContainerWidth] = React.useState(600);
    const levelHeight = 80;
    const maxSvgWidth = 700;
    const topMargin = 40;

    React.useEffect(() => {
        let running = true;
        const handleResize = () => {
            if (!running) return;
            if (containerRef.current) {
                const w = Math.min(containerRef.current.offsetWidth, maxSvgWidth);
                setContainerWidth(w);
            }
        };
        handleResize();
        let ro: ResizeObserver | null = null;
        if (window.ResizeObserver && containerRef.current) {
            ro = new window.ResizeObserver(handleResize);
            ro.observe(containerRef.current);
        }
        return () => {
            running = false;
            if (ro && containerRef.current) ro.unobserve(containerRef.current);
        };
    }, []);

    if (!node) return null;
    const { nodes, maxDepth } = layoutTreeResponsive(node, levelHeight);
    // Escala posiciones relativas al ancho real
    const scaledNodes = nodes.map(n => ({ ...n, x: n.relX * containerWidth, y: n.y + topMargin }));
    const nodeMap: Record<string, typeof scaledNodes[0]> = {};
    scaledNodes.forEach(n => { nodeMap[n.id] = n; });

    return (
        <div ref={containerRef} style={{ width: "100%", minWidth: 320, maxWidth: maxSvgWidth, margin: "0 auto", overflowX: "auto", padding: 16 }}>
            <svg width={containerWidth} height={(maxDepth + 1) * levelHeight + 60 + topMargin} style={{ display: "block", margin: "0 auto" }}>
                {/* Flechas/lineas */}
                {scaledNodes.map(n => (
                    n.parentId ? (
                        <motion.line
                            key={n.id + "-line"}
                            x1={nodeMap[n.parentId].x}
                            y1={nodeMap[n.parentId].y + 30}
                            x2={n.x}
                            y2={n.y - 30}
                            stroke="#1aaf5d"
                            strokeWidth={3}
                            initial={{ pathLength: 0 }}
                            animate={{ pathLength: 1 }}
                            transition={{ duration: 0.5 }}
                        />
                    ) : null
                ))}
                {/* Nodos */}
                {scaledNodes.map(n => {
                    const color = n.is_free ? blockColors.free : blockColors.occupied;
                    return (
                        <motion.g
                            key={n.id}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ type: "spring", stiffness: 200, damping: 20 }}
                        >
                            <rect
                                x={n.x - 40}
                                y={n.y - 30}
                                width={80}
                                height={60}
                                rx={12}
                                fill={color}
                                stroke="#333"
                                strokeWidth={2}
                                style={{ filter: n.is_free ? "drop-shadow(0 2px 8px #b2f7b8aa)" : "drop-shadow(0 2px 8px #f7b2b2aa)" }}
                            />
                            <text
                                x={n.x}
                                y={n.y}
                                textAnchor="middle"
                                alignmentBaseline="middle"
                                fontWeight={600}
                                fontSize={16}
                                fill={n.is_free ? "#1a7f3c" : "#a12b2b"}
                            >
                                {n.is_free
                                    ? `Libre (${n.size_str || n.size + ' MB'})`
                                    : `Proceso: ${n.process} (${n.size_str || n.size + ' MB'})`}
                            </text>
                        </motion.g>
                    );
                })}
            </svg>
        </div>
    );
};

export default MemoryTree;