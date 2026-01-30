#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄小说网流量分析工具
Fanqie Novel Website Traffic Analysis Tool

此工具用于分析《独家视界：谎言必须死》在番茄小说网的流量情况
This tool analyzes the traffic of "Exclusive Vision: Lies Must Die" on Fanqie Novel website
"""

import json
import os
from datetime import datetime


class FanqieTrafficAnalyzer:
    """番茄小说网流量分析器"""
    
    def __init__(self, config_path="../config/novel_config.json"):
        """初始化分析器"""
        self.config_path = config_path
        self.config = self._load_config()
        self.novel_title = self.config.get("novel", {}).get("title", "")
        self.platforms = {}
        
    def _load_config(self):
        """加载配置文件"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), self.config_path)
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件未找到: {self.config_path}")
            return {}
    
    def check_fanqie_presence(self):
        """
        检查小说是否在番茄小说网发布
        Check if the novel is published on Fanqie Novel website
        
        Returns:
            dict: 包含平台状态信息的字典
        """
        result = {
            "platform": "番茄小说网 (Fanqie Novel)",
            "novel_title": self.novel_title,
            "checked_at": datetime.now().isoformat(),
            "status": "未检测到",  # 默认状态
            "has_traffic": False,
            "analysis": {}
        }
        
        # 检查配置中是否有平台信息
        if "platforms" in self.config:
            platforms_config = self.config["platforms"]
            if "fanqie" in platforms_config:
                fanqie_info = platforms_config["fanqie"]
                result["status"] = fanqie_info.get("status", "未知")
                result["has_traffic"] = fanqie_info.get("has_traffic", False)
                result["analysis"] = fanqie_info.get("traffic_data", {})
                
        return result
    
    def analyze_potential_traffic(self):
        """
        分析小说在番茄小说网的潜在流量
        Analyze potential traffic for the novel on Fanqie Novel website
        
        Returns:
            dict: 流量分析结果
        """
        # 获取小说基本信息
        novel_info = self.config.get("novel", {})
        planning = self.config.get("planning", {})
        
        # 计算已完成章节数
        chapters_dir = os.path.join(os.path.dirname(__file__), "../chapters")
        chapter_count = 0
        total_words = 0
        
        if os.path.exists(chapters_dir):
            chapter_files = [f for f in os.listdir(chapters_dir) if f.startswith("chapter_") and f.endswith(".md")]
            chapter_count = len(chapter_files)
            
            # 计算总字数（简单估算）
            words_per_chapter = planning.get("words_per_chapter", {}).get("min", 1800)
            total_words = chapter_count * words_per_chapter
        
        analysis = {
            "novel_title": novel_info.get("title", ""),
            "genre": novel_info.get("genre", ""),
            "tags": novel_info.get("tags", []),
            "completed_chapters": chapter_count,
            "estimated_words": total_words,
            "target_chapters": planning.get("total_chapters", {}).get("target", 110),
            "completion_rate": f"{(chapter_count / planning.get('total_chapters', {}).get('target', 110) * 100):.1f}%",
            "platform_suitability": self._evaluate_platform_suitability(novel_info),
            "traffic_potential": self._estimate_traffic_potential(chapter_count, novel_info)
        }
        
        return analysis
    
    def _evaluate_platform_suitability(self, novel_info):
        """
        评估小说对番茄小说网的适配度
        Evaluate the novel's suitability for Fanqie Novel website
        """
        tags = novel_info.get("tags", [])
        genre = novel_info.get("genre", "")
        
        # 番茄小说网偏好的类型
        preferred_genres = ["都市职场", "爽文", "短剧改编"]
        preferred_tags = ["公关", "商业", "系统", "短剧"]
        
        suitability_score = 0
        reasons = []
        
        # 检查类型匹配
        if genre in preferred_genres:
            suitability_score += 30
            reasons.append(f"类型匹配: {genre}")
        
        # 检查标签匹配
        matching_tags = [tag for tag in tags if any(pt in tag for pt in preferred_tags)]
        if matching_tags:
            suitability_score += len(matching_tags) * 15
            reasons.append(f"标签匹配: {', '.join(matching_tags)}")
        
        # 短剧改编特性
        if "短剧改编" in tags or "短剧" in tags:
            suitability_score += 25
            reasons.append("具有短剧改编潜力（番茄平台优势）")
        
        suitability_level = "低"
        if suitability_score >= 70:
            suitability_level = "高"
        elif suitability_score >= 40:
            suitability_level = "中"
        
        return {
            "score": min(suitability_score, 100),
            "level": suitability_level,
            "reasons": reasons
        }
    
    def _estimate_traffic_potential(self, chapter_count, novel_info):
        """
        预估流量潜力
        Estimate traffic potential
        """
        potential = {
            "status": "未发布",
            "recommendation": []
        }
        
        if chapter_count < 10:
            potential["status"] = "内容不足"
            potential["recommendation"].append("建议至少完成30章后再发布，以保持更新吸引力")
        elif chapter_count < 30:
            potential["status"] = "可以测试发布"
            potential["recommendation"].append("内容基础已具备，可小范围测试市场反应")
        elif chapter_count >= 30:
            potential["status"] = "适合正式发布"
            potential["recommendation"].append("内容充足，建议正式发布并保持稳定更新")
            
            if chapter_count >= 50:
                potential["recommendation"].append("已有大量章节储备，可以采用爆更策略吸引读者")
        
        # 检查类型适配性
        tags = novel_info.get("tags", [])
        if "短剧改编" in tags:
            potential["recommendation"].append("短剧改编特性与番茄平台契合度高，建议重点推广")
        
        if "系统" in tags or any("系统" in tag for tag in tags):
            potential["recommendation"].append("系统流小说在番茄平台受欢迎，有流量潜力")
        
        return potential
    
    def generate_report(self):
        """
        生成完整的流量分析报告
        Generate a complete traffic analysis report
        """
        print("=" * 60)
        print(f"番茄小说网流量分析报告")
        print(f"Fanqie Novel Website Traffic Analysis Report")
        print("=" * 60)
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 检查平台发布状态
        presence = self.check_fanqie_presence()
        print(f"📚 小说名称: {presence['novel_title']}")
        print(f"📱 平台: {presence['platform']}")
        print(f"📊 发布状态: {presence['status']}")
        print(f"🔍 是否有流量: {'是' if presence['has_traffic'] else '否'}")
        print()
        
        # 分析潜在流量
        analysis = self.analyze_potential_traffic()
        print("=" * 60)
        print("📈 流量潜力分析")
        print("=" * 60)
        print(f"类型: {analysis['genre']}")
        print(f"标签: {', '.join(analysis['tags'])}")
        print(f"已完成章节: {analysis['completed_chapters']} / {analysis['target_chapters']}")
        print(f"完成度: {analysis['completion_rate']}")
        print(f"预估字数: {analysis['estimated_words']:,} 字")
        print()
        
        # 平台适配度
        suitability = analysis['platform_suitability']
        print("=" * 60)
        print("🎯 平台适配度评估")
        print("=" * 60)
        print(f"适配分数: {suitability['score']}/100")
        print(f"适配等级: {suitability['level']}")
        if suitability['reasons']:
            print("适配原因:")
            for reason in suitability['reasons']:
                print(f"  ✓ {reason}")
        print()
        
        # 流量潜力
        potential = analysis['traffic_potential']
        print("=" * 60)
        print("💡 流量潜力与建议")
        print("=" * 60)
        print(f"当前状态: {potential['status']}")
        if potential['recommendation']:
            print("建议:")
            for i, rec in enumerate(potential['recommendation'], 1):
                print(f"  {i}. {rec}")
        print()
        
        print("=" * 60)
        print("📝 总结")
        print("=" * 60)
        
        # 生成总结
        if presence['has_traffic']:
            print("✓ 该小说已在番茄小说网发布并产生流量")
        else:
            if analysis['completed_chapters'] >= 30:
                print(f"✓ 小说已完成 {analysis['completed_chapters']} 章，内容充足")
                print(f"✓ 平台适配度为 {suitability['level']}（{suitability['score']}/100）")
                print("✓ 建议发布到番茄小说网以测试市场反应")
            else:
                print(f"⚠ 小说当前完成 {analysis['completed_chapters']} 章")
                print("⚠ 建议继续创作，积累更多章节后再发布")
        
        print("=" * 60)
        
        return {
            "presence": presence,
            "analysis": analysis
        }


def main():
    """主函数"""
    analyzer = FanqieTrafficAnalyzer()
    analyzer.generate_report()


if __name__ == "__main__":
    main()
