export type Alert = {
  id: number;
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

export type Event = {
  id: number;
  event_id: string;
  timestamp: string;
  user_principal_name: string;
  event_type: string;
  ip_address: string;
  country: string;
  city: string;
  application: string;
  status: string;
  operation: string;
};