# features.py - for DOMAIN analysis only
import tldextract

def extract_features(domain):
    ext = tldextract.extract(domain)
    subdomain = ext.subdomain
    domain_name = ext.domain
    suffix = ext.suffix
    full_domain = f"{domain_name}.{suffix}"

    # 特徵提取
    length = len(domain)
    has_dash = "-" in domain
    num_dots = domain.count(".")
    sub_length = len(subdomain) if subdomain else 0

    # 是否含疑似詐騙關鍵字
    phishing_keywords = ["claim", "airdrop", "connect", "wallet", "verify", "app", "login"]
    has_phishing_keyword = int(any(kw in domain.lower() for kw in phishing_keywords))

    return [
        length,
        int(has_dash),
        num_dots,
        sub_length,
        has_phishing_keyword
    ]
