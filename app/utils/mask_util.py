import re
from typing import Any


class MaskUtil:
    """
    敏感数据脱敏工具类
    支持常见字段的掩码处理，适用于 API 响应、日志打印等场景。
    """

    @staticmethod
    def phone(value: str | None) -> str:
        """手机号脱敏：13812345678 → 138****5678"""
        if not value:
            return ""
        clean = re.sub(r"\D", "", str(value))
        if len(clean) == 11:
            return f"{clean[:3]}****{clean[7:]}"
        return clean

    @staticmethod
    def email(value: str | None) -> str:
        """邮箱脱敏：abc@example.com → a**c@example.com"""
        if not value or "@" not in str(value):
            return ""
        local, domain = str(value).rsplit("@", 1)
        if len(local) <= 2:
            masked_local = local[0] + "*" * (len(local) - 1)
        else:
            masked_local = local[0] + "**" + local[-1]
        return f"{masked_local}@{domain}"

    @staticmethod
    def id_card(value: str | None) -> str:
        """身份证脱敏：110101199003071234 → 110101********1234"""
        if not value:
            return ""
        clean = re.sub(r"\s+", "", str(value))
        if len(clean) == 18:
            return f"{clean[:6]}********{clean[14:]}"
        return clean

    @staticmethod
    def bank_card(value: str | None) -> str:
        """银行卡脱敏：6222081234567890123 → **** **** **** 0123"""
        if not value:
            return ""
        clean = re.sub(r"\D", "", str(value))
        if len(clean) >= 4:
            groups = [clean[i : i + 4] for i in range(0, len(clean), 4)]
            masked_groups = ["****"] * (len(groups) - 1) + [groups[-1]]
            return " ".join(masked_groups)
        return clean

    @staticmethod
    def name(value: str | None) -> str:
        """姓名脱敏：
        - 单字：张 → 张
        - 双字：张三 → 张*
        - 多字：欧阳小明 → 欧阳**明
        """
        if not value:
            return ""
        name = str(value).strip()
        if len(name) == 1:
            return name
        elif len(name) == 2:
            return name[0] + "*"
        else:
            return name[:2] + "*" * (len(name) - 3) + name[-1]

    @staticmethod
    def address(value: str | None) -> str:
        """地址脱敏：北京市朝阳区建国路123号 → 北京市朝阳区******123号"""
        if not value:
            return ""
        addr = str(value)
        if len(addr) <= 6:
            return addr
        # 保留前6个字符和最后3个字符，中间用*代替
        return addr[:6] + "******" + addr[-3:]

    @staticmethod
    def generic(
        value: Any | None, keep_head: int = 2, keep_tail: int = 2, mask_char: str = "*"
    ) -> str:
        """通用脱敏：适用于任意字符串
        示例：generic("1234567890", 3, 3) → 123***890
        """
        if value is None:
            return ""
        s = str(value)
        total = len(s)
        if total <= keep_head + keep_tail:
            return mask_char * total
        masked_len = total - keep_head - keep_tail
        return s[:keep_head] + mask_char * masked_len + s[-keep_tail:]
