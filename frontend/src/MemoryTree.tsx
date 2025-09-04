import { motion } from "framer-motion";

export interface MemoryNode {
    size: number;
    size_str?: string;
    is_free: boolean;
    process: string | null;
    left: MemoryNode | null;
    right: MemoryNode | null;
}

interface MemoryTreeProps {
    node: MemoryNode;
}

const blockColors = {
    free: "#b2f7b8",
    occupied: "#f7b2b2",
};

// Helper: BFS traversal to get nodes by level
function getLevels(root: MemoryNode): MemoryNode[][] {
    const levels: MemoryNode[][] = [];
    let queue: { node: MemoryNode; level: number }[] = [{ node: root, level: 0 }];
    while (queue.length > 0) {
        const { node, level } = queue.shift()!;
        if (!levels[level]) levels[level] = [];
        levels[level].push(node);
        if (node.left && node.right) {
            queue.push({ node: node.left, level: level + 1 });
            queue.push({ node: node.right, level: level + 1 });
        }
    }
    return levels;
}

const MemoryTree: React.FC<MemoryTreeProps> = ({ node }) => {
    if (!node) return null;
    const totalSize = node.size;
    const levels = getLevels(node);

    return (
        <div style={{ width: "100%", overflowX: "auto", padding: 16 }}>
            {levels.map((level, i) => (
                <div
                    key={i}
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "center",
                        alignItems: "flex-end",
                        marginBottom: 12,
                        gap: 8,
                    }}
                >
                    {level.map((block, j) => {
                        const color = block.is_free ? blockColors.free : blockColors.occupied;
                        // Ancho proporcional al tamaño del bloque respecto al total
                        const widthPercent = (block.size / totalSize) * 100;
                        return (
                            <motion.div
                                key={block.process ? `proc-${block.process}` : `free-${block.size}-${i}-${j}`}
                                initial={{ scaleY: 0.8, opacity: 0 }}
                                animate={{ scaleY: 1, opacity: 1, backgroundColor: color }}
                                exit={{ scaleY: 0.8, opacity: 0 }}
                                transition={{ type: "spring", stiffness: 200, damping: 20 }}
                                style={{
                                    border: "2px solid #333",
                                    background: color,
                                    minWidth: 40,
                                    width: `${widthPercent}%`,
                                    maxWidth: 300,
                                    height: 40,
                                    borderRadius: 8,
                                    textAlign: "center",
                                    boxShadow: block.is_free ? "0 2px 8px #b2f7b8aa" : "0 2px 8px #f7b2b2aa",
                                    position: "relative",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    fontWeight: 600,
                                    fontSize: 15,
                                    overflow: "hidden",
                                }}
                                title={
                                    block.is_free
                                        ? `Libre (${block.size_str || block.size + ' MB'})`
                                        : `Proceso: ${block.process} (${block.size_str || block.size + ' MB'})`
                                }
                            >
                                {block.is_free
                                    ? `Libre (${block.size_str || block.size + ' MB'})`
                                    : `Proceso: ${block.process} (${block.size_str || block.size + ' MB'})`}
                            </motion.div>
                        );
                    })}
                </div>
            ))}
        </div>
    );
};

export default MemoryTree;