/**
 * @file config
 * @author wheel-w
 */

import path from 'path'
import prodEnv from './prod.env'
import devEnv from './dev.env'

export default {
    build: {
        // env 会通过 webpack.DefinePlugin 注入到前端代码里
        env: prodEnv,
        assetsRoot: path.resolve(__dirname, '../../static/apply_dist'),
        assetsSubDirectory: 'static',
        assetsPublicPath: '{{BK_APPLY_STATIC_URL}}',
        productionSourceMap: true,
        productionGzip: false,
        productionGzipExtensions: ['js', 'css'],
        bundleAnalyzerReport: process.env.npm_config_report
    },
    dev: {
        // env 会通过 webpack.DefinePlugin 注入到前端代码里
        env: devEnv,
        // 这里用 JSON.parse 是因为 dev.env.js 里有一次 JSON.stringify，dev.env.js 里的 JSON.stringify 不能去掉
        localDevUrl: JSON.parse(devEnv.LOCAL_DEV_URL),
        localDevPort: JSON.parse(devEnv.LOCAL_DEV_PORT),
        assetsSubDirectory: 'static',
        assetsPublicPath: '/',
        proxyTable: {
            '/bk_api': {  //代理地址
                target: 'http://dev.paas-edu.bktencent.com:8000',  //需要代理的地址， 实际生产环境需要访问的地址
                changeOrigin: true,  //是否跨域
                secure: false,
                pathRewrite: {
                    '^/bk_api': ''   //本身的接口地址没有 '/bk_api' 这种通用前缀，所以要rewrite，如果本身有则去掉
                }
            }
        },
        cssSourceMap: false,
        autoOpenBrowser: false
    }
}
