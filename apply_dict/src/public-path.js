/**
 * @file webpack public path config
 * @author wheel-w
 */

// eslint-disable-next-line
__webpack_public_path__ = window.PROJECT_CONFIG.BK_APPLY_STATIC_URL + '/'
// __webpack_public_path__ = window.PROJECT_CONFIG.BK_STATIC_URL + '/'// 线下跑的时候得把"/"去掉，提交到线上则需要加回去，
