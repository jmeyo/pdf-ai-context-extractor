"""
Locale detection and configuration for multi-language PDF extraction.

Supports French (fr), German (de), and English (en) with automatic detection
from filename and content.
"""

import re
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
import pandas as pd
from dataclasses import dataclass


@dataclass
class LocaleConfig:
    """Configuration for a specific locale."""

    code: str
    name: str
    date_patterns: list  # Regex patterns for date formats
    amount_patterns: list  # Regex patterns for amounts
    decimal_separator: str  # ',' or '.'
    thousands_separator: str  # ' ', '.', or ','
    keywords: list  # Common words in this language

    def __repr__(self):
        return f"LocaleConfig({self.code}, {self.name})"


# Locale configurations
LOCALES: Dict[str, LocaleConfig] = {
    'fr': LocaleConfig(
        code='fr',
        name='French',
        date_patterns=[
            r'\d{1,2}/\d{1,2}/\d{4}',  # DD/MM/YYYY
            r'\d{1,2}\.\d{1,2}\.\d{4}',  # DD.MM.YYYY
            r'\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}',
        ],
        amount_patterns=[
            r'[+-]?\s*\d+[\s,]\d{2}\s*€?',  # 1 234,56 or 1234,56
            r'[+-]?\s*\d+,\d{2}\s*EUR',
        ],
        decimal_separator=',',
        thousands_separator=' ',
        keywords=[
            'solde', 'crédit', 'débit', 'virement', 'prélèvement',
            'montant', 'date', 'opération', 'facture', 'relevé',
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
    ),

    'de': LocaleConfig(
        code='de',
        name='German',
        date_patterns=[
            r'\d{1,2}\.\d{1,2}\.\d{4}',  # DD.MM.YYYY
            r'\d{1,2}/\d{1,2}/\d{4}',  # DD/MM/YYYY
            r'\d{1,2}\s+(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}',
        ],
        amount_patterns=[
            r'[+-]?\s*\d+[\.,]\d{3}[\.,]\d{2}',  # 1.234,56 or 1,234.56
            r'[+-]?\s*\d+,\d{2}\s*€?',
            r'[+-]?\s*\d+,\d{2}\s*EUR',
        ],
        decimal_separator=',',
        thousands_separator='.',
        keywords=[
            'saldo', 'kredit', 'lastschrift', 'überweisung', 'betrag',
            'datum', 'buchung', 'rechnung', 'kontoauszug',
            'januar', 'februar', 'märz', 'april', 'mai', 'juni',
            'juli', 'august', 'september', 'oktober', 'november', 'dezember'
        ]
    ),

    'en': LocaleConfig(
        code='en',
        name='English',
        date_patterns=[
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
        ],
        amount_patterns=[
            r'[+-]?\s*\$?\d+,\d{3}\.\d{2}',  # $1,234.56
            r'[+-]?\s*\d+\.\d{2}\s*(?:USD|EUR|GBP)?',
        ],
        decimal_separator='.',
        thousands_separator=',',
        keywords=[
            'balance', 'credit', 'debit', 'transfer', 'payment',
            'amount', 'date', 'transaction', 'invoice', 'statement',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
    ),
}


class LocaleDetector:
    """Detect and manage locale for PDF extraction."""

    def __init__(self, default_locale: str = 'fr'):
        """
        Initialize locale detector.

        Args:
            default_locale: Default locale code ('fr', 'de', 'en')
        """
        if default_locale not in LOCALES:
            raise ValueError(f"Unknown locale: {default_locale}. Available: {list(LOCALES.keys())}")

        self.default_locale = default_locale
        self._confidence_threshold = 0.3  # Minimum confidence to detect locale

    def detect_from_filename(self, filename: str) -> Optional[str]:
        """
        Detect locale from filename patterns.

        Args:
            filename: PDF filename

        Returns:
            Detected locale code or None
        """
        filename_lower = filename.lower()

        # Language indicators in filename
        lang_indicators = {
            'fr': ['_fr', '-fr', 'french', 'francais', 'français', 'france'],
            'de': ['_de', '-de', 'german', 'deutsch', 'deutschland', 'germany'],
            'en': ['_en', '-en', 'english', 'uk', 'usa', 'us'],
        }

        for locale, indicators in lang_indicators.items():
            if any(ind in filename_lower for ind in indicators):
                return locale

        return None

    def detect_from_content(self, df: pd.DataFrame) -> Tuple[Optional[str], float]:
        """
        Detect locale from DataFrame content using keyword matching.

        Args:
            df: Extracted DataFrame

        Returns:
            Tuple of (detected locale code, confidence score)
        """
        if df is None or df.empty:
            return None, 0.0

        # Concatenate all text content
        text = ' '.join(
            str(val).lower()
            for row in df.values
            for val in row
            if pd.notna(val)
        )

        if not text:
            return None, 0.0

        # Count keyword matches for each locale
        scores = {}
        for locale_code, config in LOCALES.items():
            keyword_count = sum(
                1 for keyword in config.keywords
                if keyword.lower() in text
            )
            # Normalize by number of keywords
            scores[locale_code] = keyword_count / len(config.keywords)

        if not scores:
            return None, 0.0

        # Get best match
        best_locale = max(scores, key=scores.get)
        confidence = scores[best_locale]

        # Only return if confidence is above threshold
        if confidence >= self._confidence_threshold:
            return best_locale, confidence

        return None, confidence

    def detect_locale(
        self,
        filename: str,
        df: Optional[pd.DataFrame] = None,
        explicit_locale: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Detect locale using multiple strategies.

        Priority:
        1. Explicit locale parameter
        2. Filename pattern
        3. Content analysis
        4. Default locale

        Args:
            filename: PDF filename
            df: Extracted DataFrame (for content analysis)
            explicit_locale: Explicitly specified locale

        Returns:
            Tuple of (locale code, detection method)
        """
        # 1. Explicit locale
        if explicit_locale:
            if explicit_locale in LOCALES:
                return explicit_locale, 'explicit'
            else:
                print(f"⚠️  Unknown locale '{explicit_locale}', using default")

        # 2. Filename pattern
        filename_locale = self.detect_from_filename(filename)
        if filename_locale:
            return filename_locale, 'filename'

        # 3. Content analysis
        if df is not None:
            content_locale, confidence = self.detect_from_content(df)
            if content_locale:
                return content_locale, f'content (confidence: {confidence:.2%})'

        # 4. Default
        return self.default_locale, 'default'

    def get_config(self, locale: str) -> LocaleConfig:
        """Get configuration for a locale."""
        return LOCALES.get(locale, LOCALES[self.default_locale])


def clean_amount(
    text: str,
    locale: str = 'fr',
    locale_config: Optional[LocaleConfig] = None
) -> Optional[float]:
    """
    Clean and convert amount strings to float based on locale.

    Args:
        text: Amount text
        locale: Locale code
        locale_config: Optional LocaleConfig (avoids lookup)

    Returns:
        Float value or None
    """
    if pd.isna(text) or text == '':
        return None

    if locale_config is None:
        locale_config = LOCALES.get(locale, LOCALES['fr'])

    text = str(text).strip()

    # Remove currency symbols
    text = re.sub(r'[€$£¥]', '', text)
    text = re.sub(r'EUR|USD|GBP|CHF', '', text, flags=re.IGNORECASE)

    # Remove spaces
    text = text.replace(' ', '')

    # Handle locale-specific formatting
    if locale_config.decimal_separator == ',':
        # French/German: 1.234,56 or 1 234,56
        # Remove thousands separator
        text = text.replace(locale_config.thousands_separator, '')
        # Replace decimal separator
        text = text.replace(',', '.')
    else:
        # English: 1,234.56
        # Remove thousands separator
        text = text.replace(locale_config.thousands_separator, '')

    # Remove + signs
    text = text.replace('+', '')

    try:
        return float(text)
    except ValueError:
        return None


def parse_date(
    text: str,
    locale: str = 'fr',
    locale_config: Optional[LocaleConfig] = None
) -> Optional[str]:
    """
    Parse date string based on locale.

    Args:
        text: Date text
        locale: Locale code
        locale_config: Optional LocaleConfig

    Returns:
        Standardized date string (DD/MM/YYYY) or None
    """
    if pd.isna(text) or not text:
        return None

    if locale_config is None:
        locale_config = LOCALES.get(locale, LOCALES['fr'])

    text = str(text).strip()

    # Try each date pattern for this locale
    for pattern in locale_config.date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None


# Convenience function for checking available locales
def list_available_locales() -> Dict[str, str]:
    """List all available locales."""
    return {code: config.name for code, config in LOCALES.items()}
