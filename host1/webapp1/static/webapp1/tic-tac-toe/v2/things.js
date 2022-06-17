// +--------
// | 石
// |

/**
 * PC は Piece （駒，石 などの意味）の略です
 * @type {number}
 */
const PC_EMPTY = 0; // Pieceがないことを表します
const PC_X = 1;
const PC_O = 2;

/**
 * ラベル
 * @type {string}
 */
const PC_EMPTY_LABEL = "";
const PC_X_LABEL = "X";
const PC_O_LABEL = "O";

// |
// | 石
// +--------

// +--------
// | 盤
// |

/**
 * 盤上の升の数
 * @type {number}
 */
const BOARD_AREA = 9;

/**
 * SQ は Square （マス）の略です
 * +---------+
 * | 0  1  2 |
 * | 3  4  5 |
 * | 6  7  8 |
 * +---------+
 * @type {number}
 */
const SQ_0 = 0;
const SQ_1 = 1;
const SQ_2 = 2;
const SQ_3 = 3;
const SQ_4 = 4;
const SQ_5 = 5;
const SQ_6 = 6;
const SQ_7 = 7;
const SQ_8 = 8;

// | 盤
// |
// +--------
