/**
 * @file intro router 配置
 * @author wheel-w
 */

const Introduction = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/introduction.md')
const InstallAndUsage = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/install-and-usage.md')
const QuestionExplain = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/question-explain.md')
const CommandInit = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/command-init.md')
const CommandHelp = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/command-help.md')
const CommandVersion = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/command-version.md')
const Webpack4DirExplain = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/webpack4-dir-explain.md')
const ConfigExplain = () => import(/* webpackChunkName: 'intro' */'@doc/views/intro/config-explain.md')

export default [
    {
        path: '/introduction',
        alias: '',
        name: 'introduction',
        component: Introduction
    },
    {
        path: '/install-and-usage',
        name: 'installAndUsage',
        component: InstallAndUsage
    },
    {
        path: '/command-init',
        name: 'commandInit',
        component: CommandInit
    },
    {
        path: '/command-help',
        name: 'commandHelp',
        component: CommandHelp
    },
    {
        path: '/command-version',
        name: 'commandVersion',
        component: CommandVersion
    },
    {
        path: '/question-explain',
        name: 'questionExplain',
        component: QuestionExplain
    },
    {
        path: '/webpack4-dir-explain',
        name: 'webpack4DirExplain',
        component: Webpack4DirExplain
    },
    {
        path: '/config-explain',
        name: 'configExplain',
        component: ConfigExplain
    }
]
