export type UploadBatch = {
  id: number;
  upload_batch_uuid: string;
  original_filename: string;
  event_count: number;
  created_at: string;
};

export type Alert = {
  id: number;
  upload_batch_uuid: string;
  rule_id: string;
  rule_name: string;
  title: string;
  description: string;
  severity: string;
  score: number;
  affected_user: string;
  source_ip: string;
  mitre_technique_id: string;
  mitre_technique_name: string;
  evidence: string;
  created_at: string;
};

export type Case = {
  id: number;
  upload_batch_uuid: string;
  title: string;
  status: string;
  severity: string;
  score: number;
  affected_user: string;
  summary: string;
  recommendations: string;
  related_alert_ids: string;
  created_at: string;
  updated_at: string;
};

export type CaseComment = {
  id: number;
  case_id: number;
  comment: string;
  created_at: string;
};

export type Event = {
  id: number;
  upload_batch_uuid: string;
  event_id: string;
  timestamp: string;
  user_principal_name: string;
  event_type: string;
  ip_address: string;
  country: string;
  city: string;
  user_agent: string;
  application: string;
  status: string;
  failure_reason: string;
  mfa_result: string;
  client_app: string;
  operation: string;
  target_resource: string;
  details: string;
};