#!/usr/bin/env python3
"""Check declared content coverage and panel mappings before building a PPTX.

This checks the plan, not the paper's completeness or the rendered presentation.
Errors exit 1. Panel counts are not quality scores.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def audit(plan):
    report = {
        'errors': [], 'warnings': [], 'visible_content_ids': [],
        'boundary': '仅核对计划内的声明和映射；须另行对照论文清单及实际幻灯片，不是信息密度评分。',
    }

    def error(code, message):
        report['errors'].append({'code': code, 'message': message})

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def positive_int(value):
        return type(value) is int and value > 0

    if not isinstance(plan, dict):
        error('invalid_plan', 'Plan must be an object')
        return report
    inventory = plan.get('content_inventory')
    slides = plan.get('slides')
    if not isinstance(inventory, list) or not inventory:
        error('invalid_inventory', 'Non-empty content_inventory is required')
        inventory = []
    if not isinstance(slides, list) or not slides:
        error('invalid_slides', 'Non-empty slides is required')
        slides = []
    items = {}
    for index, item in enumerate(inventory):
        if not isinstance(item, dict) or not text(item.get('id')):
            error('invalid_content', f'Content {index + 1} needs a non-empty id')
            continue
        key = item['id']
        if key in items:
            error('duplicate_content', f'Duplicate content id: {key}')
            continue
        items[key] = item
        if not text(item.get('topic')) or not text(item.get('source')):
            error('missing_source_or_topic', f'{key}: topic and source locator are required')
        if type(item.get('required_on_slide')) is not bool:
            error('invalid_requirement', f'{key}: required_on_slide must be a boolean')

    visible = set()
    for index, slide in enumerate(slides, 1):
        if not isinstance(slide, dict):
            error('invalid_slide', f'Slide {index} must be an object')
            continue
        if type(slide.get('slide')) is not int or slide['slide'] != index:
            error('invalid_slide_order', f'Expected slide number {index}')
        panels = slide.get('panels')
        if not isinstance(panels, list) or not panels:
            error('missing_panels', f'Slide {index}: explicit content panels required')
            continue
        labels = set()
        for panel in panels:
            if not isinstance(panel, dict):
                error('invalid_panel', f'Slide {index}: panel must be an object')
                continue
            label = panel.get('label')
            if not text(label) or label in labels:
                error('invalid_panel_label', f'Slide {index}: panel labels must be non-empty and unique')
            else:
                labels.add(label)
            points = panel.get('key_points')
            if (not text(panel.get('title')) or not text(panel.get('visual')) or
                    not isinstance(points, list) or not points or not all(text(p) for p in points)):
                error('empty_panel', f'Slide {index}/{label}: title, visual and substantive key_points required')
            ids = panel.get('content_ids')
            if not isinstance(ids, list) or not ids:
                error('missing_content_ids', f'Slide {index}/{label}: content_ids required')
                continue
            for key in ids:
                if not isinstance(key, str) or key not in items:
                    error('unknown_content', f'Slide {index}/{label}: unknown content id {key!r}')
                else:
                    visible.add(key)

    for key, item in items.items():
        if item.get('required_on_slide') is True and key not in visible:
            error('missing_visible_content', f'{key}: required content has no visible panel; notes do not count')
        if item.get('required_on_slide') is False and key not in visible and not text(item.get('exclusion_reason')):
            error('unexplained_exclusion', f'{key}: excluded supplemental content needs a reason')

    for field in ('figure_usage', 'equations'):
        entries = plan.get(field, [])
        if not isinstance(entries, list):
            error('invalid_visual_inventory', f'{field} must be a list')
            continue
        seen = set()
        for item in entries:
            if not isinstance(item, dict) or not text(item.get('id')) or not text(item.get('source')):
                error('invalid_visual_entry', f'{field}: id and source required')
                continue
            if item['id'] in seen:
                error('duplicate_visual', f'{field}: duplicate id {item["id"]}')
            seen.add(item['id'])
            assigned = item.get('slides', [])
            if not isinstance(assigned, list) or any(not positive_int(n) or n > len(slides) for n in assigned):
                error('invalid_visual_slide', f'{item["id"]}: invalid slide references')
            elif assigned:
                if not text(item.get('purpose')):
                    error('missing_visual_purpose', f'{item["id"]}: explain what the visible visual contributes')
                if field == 'figure_usage' and not text(item.get('route')):
                    error('missing_figure_route', f'{item["id"]}: extraction or reconstruction route required')
            elif not text(item.get('exclusion_reason')):
                error('unexplained_visual_exclusion', f'{item["id"]}: unused visual needs a reason')

    deck = plan.get('deck')
    if not isinstance(deck, dict):
        error('invalid_deck', 'deck settings required')
    else:
        planned = deck.get('planned_slide_count')
        if not positive_int(planned) or planned != len(slides):
            error('planned_count_mismatch', 'planned_slide_count must equal the number of slides')
        requested = deck.get('requested_slide_count')
        if requested is not None and (not positive_int(requested) or requested != len(slides)):
            error('requested_count_mismatch', 'Explicit requested_slide_count must match the number of slides')
    report['visible_content_ids'] = sorted(visible)
    report['content_count'] = len(items)
    report['slide_count'] = len(slides)
    return report


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report and args.report.resolve() == args.input.resolve():
        parser.error('--report must not overwrite the input plan')
    try:
        report = audit(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as exc:
        report = {'errors': [{'code': 'unreadable_plan', 'message': str(exc)}], 'warnings': []}
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    return 1 if report['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
