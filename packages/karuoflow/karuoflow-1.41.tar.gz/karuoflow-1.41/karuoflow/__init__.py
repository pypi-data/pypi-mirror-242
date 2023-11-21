# -*- encoding: utf-8 -*-
'''
@文件    :__init__.py
@说明    :
@时间    :2020/09/02 16:27:09
@作者    :caimmy@hotmail.com
@版本    :0.1
'''


from .flowapp import KaruoFlow
from .db.tables import InitKaruoflowTables
from .datadef import DbConfig

'''
@version 0.6 [2021-05-26] 增加会签、加签(InsertSign)、转签(AddSign)等功能
@version 0.7 [2021-06-10] 增加直接转入下一阶段的功能，供业务层决定阶段变更
@version 0.8 [2021-06-15] 审批接口 AgreeJobFlow_V2 增加手写签名参数
@version 0.9 [2021-08-26] 支持同一个审核人的连续审批
@version 0.91 [2021-09-25] 修复连续审批过程中的一个bug，当连续审批遇到会签阶段时，需要跳出循环，避免循环死锁
@version 0.92, 0.93 [2021-09-25] 优化报错信息
@version 1.0 [2021-09-25] 支持查询指定流程指定阶段的决策记录
@version 1.1 [2021-09-28] 修正会签处理bug(避免会签阶段审核人反复审签)
@version 1.2 [2021-09-30] 增加接口，修改审批任务当前审批人列表
@version 1.21 [2021-10-12] 修复根据yml模板初始话流程的bug
@version 1.22 [2021-10-18] 增加 QueryJobViaRelationPrimaryKey 接口，已审核数据增加除重
@version 1.23 [2021-10-18] 增加 QueryJobViaRelationPrimaryKey 接口，已审核数据增加除重
@version 1.24 [2021-12-01] 修复bug，获取待审核列表时，排序未生效
@version 1.25 [2022-03-10] 增加AppendSign 接口，供批量追加审核节点，（多能上会申请定制化场景需求）
@version 1.26 [2022-03-14] 修正了查询已审核申请列表数据问题，该问题由关联查询引起，但模糊匹配仍然存在问题
@version 1.27 [2022-03-14] 修正了1.26版本中join查询的条件bug
@version 1.28 [2022-11-06] 针对sqlalchemy的缓存问题，对db操作包裹db_session.begin()事务上下文
@version 1.29 [2022-11-06] 针对sqlalchemy的缓存问题，对db操作包裹db_session.begin()事务上下文，该机制因为在外部系统中传入了session，并在传入前开启了事务，因此会报错，先退回。
@version 1.30 [2023-05-12] 增加更新ext_data字段的函数
@version 1.31 [2023-06-01] 修改AddSign函数的签名，增加传入name和node_label两个参数
@version 1.32 [2023-06-16] 在审批流查询中增加观察员角色
@version 1.33 [2023-09-12] 查询审批流的时候支持abstract[摘要字段]的模糊查询
@version 1.34 [2023-09-24] 审核结点支持上传附件等操作
@version 1.35 [2023-09-24] 增加自由检索申请单接口
@version 1.36 [2023-11-08] 流程查询接口增强，支持catalog多选、按申请发起日期查询
@version 1.37 [2023-11-09] 强化观察员角色的查询功能
@version 1.38 [2023-11-09] fix bug
@version 1.39 [2023-11-09] fix bug
@version 1.40 [2023-11-16] fix bug
@version 1.41 [2023-11-21] 支持观察员传入流程申请人列表，过滤符合申请人条件的申请单
'''

__version__ = 1.41