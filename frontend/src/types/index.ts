export interface ResponseMetadata {
  source_email: string;
  timestamp_processed: string;
}

export interface LineItem {
  product_name: string;
  quantity: number;
  unit_price?: number;
  item_code?: string;
}

export interface ExtractionResult {
  vendor_name?: string;
  invoice_number?: string;
  raw_total?: number;
  applied_discount_percentage?: number;
  invoice_final_total?: number;
  is_urgent: boolean;
  routing_instruction?: string;
  invoice_line_items: LineItem[];
  delivery_line_items: LineItem[];
  confidence_score?: number; // Depending on where it's stored
}

export interface ValidationResult {
  required_fields_valid: boolean;
  invoice_number_valid: boolean;
  vendor_exists: boolean;
  price_calculation_valid: boolean;
  line_items_match_delivery: boolean;
  final_calculated_total?: number;
  confidence_score: number;
  errors: string[];
  warnings: string[];
}

export interface ProcessResponse {
  metadata: ResponseMetadata;
  extraction: ExtractionResult;
  validation: ValidationResult;
  workflow_action: string;
}

export interface ProcessingJob {
  job_id: string;
  status: string;
  metadata: ResponseMetadata;
  attachments: any[];
  extraction?: ExtractionResult;
  validation?: ValidationResult;
  workflow_action?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface Statistics {
  total_jobs: number;
  approved_jobs: number;
  review_jobs: number;
  rejected_jobs: number;
  average_confidence: number;
}
