BEGIN;
SET CONSTRAINTS ALL DEFERRED;
DELETE FROM oppy.usuarios WHERE username = 'demo-enfermera';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('36bda099-778e-47e5-8e80-e66e83a171f4', 'demo-enfermera', 'enfermera@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Valentina', 'Fuentes');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('8144a920-9537-40fa-ab38-fa909f981e50', '36bda099-778e-47e5-8e80-e66e83a171f4', 'enfermera@demo.oppytalent.com',
                'VALENTINA FUENTES SÁNCHEZ', 'ENFERMERA', 'Enfermera titulada de la Universidad del Biobío en el año 2015, con experiencia en UPC, Urgencias, Médico Quirúrgico y docencia, entre otras áreas. Competente en manejo de pacientes críticos, cuidados paliativos, manejo de IAAS y atención de urgencias de mediana y alta complejidad. Destaco por adaptarme a diversos entornos según la visión y misión de cada empresa y resolver situaciones críticas con un enfoque centrado en el paciente y su familia, manteniendo actualización permanente de mis conocimientos para entregar la mejor atención y calidad.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/generic_nurse_avatar.webp', '+56 9 555 55 555', 'https://www.linkedin.com/in/demo01',
                NULL, NULL, 'Iquique, Chile',
                '[]', '[]',
                '["Empat\u00eda", "Trato respetuoso", "Escucha activa", "Trabajo colaborativo en equipos multidisciplinarios", "Creatividad", "Tolerancia a la frustraci\u00f3n", "Trabajo bajo presi\u00f3n", "Capacidad de adaptabilidad", "Flexibilidad al cambio", "Proactividad", "Organizaci\u00f3n", "Responsabilidad", "Motivaci\u00f3n por el logro y la calidad", "Liderazgo", "Atenci\u00f3n y orientaci\u00f3n a usuarios", "Manejo de pacientes cr\u00edticos", "Realizar maniobras de RCP", "Administraci\u00f3n de medicamentos", "Preparaci\u00f3n y administraci\u00f3n de drogas oncol\u00f3gicas y drogas vasoactivas", "Manejo de VMNI/VMI", "Manejo de cat\u00e9ter venoso central", "Manejo de invasivos", "Atenci\u00f3n de urgencias de mediana y alta complejidad", "Manejo de IAAS", "Electrocardiograma avanzada", "Arritmias", "Soporte vital avanzado (ACLS)", "Cuidados paliativos", "Manejo de confidencialidad y \u00e9tica profesional", "Gesti\u00f3n administrativa"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('1a7425ee-8853-4699-b1e5-421bb8203381', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Cuidado Integral a Domicilio Ltda.', 'Enfermera / Cuidadora de Pacientes Domiciliarios',
                    '2024-12-01', NULL, 'Realizar aseo y confort, asistir en actividades de la vida diaria, administrar cuidados básicos de enfermería, acompañar y brindar contención al paciente y familia.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('94d2deca-6b45-4048-9246-671a1cc4eeec', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Universidad Andrés Bello', 'Enfermera Docente',
                    '2024-08-01', '2024-09-01', 'Supervisar estudiantes en campos clínicos, coordinar actividades académicas, evaluar desempeño clínico y realizar labores administrativas docentes.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('2d58bede-61de-42cd-b14b-303bf55e72aa', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Red Salud Paliativa Chile', 'Enfermera – Cuidados Paliativos',
                    '2024-01-01', NULL, 'Controlar síntomas, administrar tratamientos indicados, brindar cuidados integrales al paciente, acompañar a la familia y coordinar atención interdisciplinaria.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5b7bba12-6aed-4b65-a7d2-5a19ee793d45', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Clínica Los Andes', 'Enfermera – UPC Respiratoria',
                    '2020-01-01', '2022-12-01', 'Realizar monitoreo de pacientes críticos 24/7 en UCI respiratoria por Pandemia COVID-19, manejar pacientes intubados, realizar maniobras de RCP y ejecutar labores administrativas según el cargo.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('586d1436-6000-430c-856b-6b60bb838639', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Hospital Regional de Santiago', 'Enfermera',
                    '2019-01-01', '2020-12-01', 'Realizar atención clínica de mediana y alta complejidad, preparar y administrar medicamentos, manejar catéter venoso central y apoyar procedimientos de urgencia.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('0a4e99b2-ed83-43b9-879c-94f79e20cac7', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Hospital de Carabineros de Chile', 'Enfermera – UPC Coronaria',
                    '2016-07-01', '2018-12-01', 'Preparar y administrar drogas vasoactivas, asistir en cirugía a corazón abierto con ECMO y realizar labores administrativas atingentes al servicio.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('9f8889d8-fa26-40fb-acd2-a07c6bd7e230', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Clínica Alemana de Santiago', 'Enfermera – UTI y UPC General',
                    '2016-01-01', '2018-01-01', 'Brindar cuidados a pacientes de mediana y alta complejidad, monitorizar parámetros críticos, administrar tratamientos especializados y lograr sugerir e implementar programa de prevención de lesiones por presión.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('3e4f7220-486a-480b-b73b-26bcce6c97b1', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Hospital Pediátrico Dr. Luis Calvo Mackenna', 'Enfermera – Urgencia Pediátrica',
                    '2015-04-01', '2015-07-01', 'Atender pacientes pediátricos en contexto de urgencia, administrar medicamentos, realizar cuidados clínicos básicos y apoyar procedimientos médicos.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('2e71bea1-1410-47f2-9e1b-cb19e6e21159', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Universidad Adolfo Ibáñez / Universidad Finis Terrae', 'Supervisora de Campos Clínicos',
                    '2013-01-01', '2014-12-01', 'Supervisar estudiantes en práctica, coordinar actividades clínicas, evaluar competencias profesionales y realizar labores administrativas asociadas al rol.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('9efb7e9f-856d-4cad-9521-e921bb4a2d6b', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Academia Salud Integral', 'Electrocardiograma avanzada y arritmias',
                    2018, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('fc4fd195-13f3-499e-bc67-ea6218ff48c1', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Universidad del Biobío', 'Enfermería',
                    2015, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('46807688-efd1-4ae7-b6da-c823535a49c9', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Instituto Chileno de Capacitación en Salud (ICCS)', 'BLS (Basic Life Resusitation)',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('61c298f9-6598-4027-902f-1fc4f6884044', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Instituto Chileno de Capacitación en Salud (ICCS)', 'ESI (Categorización en urgencia)',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('b8fa6a14-82ba-401c-a8d1-2b03dcb570f9', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Academia Salud Integral', 'IAAS',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d20f4b26-893f-44ca-9ce7-0679e3bd34eb', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Instituto Chileno de Capacitación en Salud (ICCS)', 'Curaciones Avanzadas',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('6e307a37-00a6-484c-b53c-b9e7e9b61c56', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Clínica de Capacitación Médica (CCM)', 'ACLS',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d174db32-6251-4301-82c8-cd09fbd847da', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Clínica de Capacitación Médica (CCM)', 'Atención Pre Hospitalaria (CAPREB)',
                    2023, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('356caab1-130e-446c-9109-f19d91596879', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Clínica de Capacitación Médica (CCM)', 'Técnicas de manipulación de equipos empleados en VMNI Y VMI',
                    2018, 'Estudio extraído', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('06288edd-1dd7-4797-9531-c2deda5236c9', '36bda099-778e-47e5-8e80-e66e83a171f4', 'Disponibilidad', 'Disponibilidad Inmediata',
                    'Detalle de la habilitación', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-profesora';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'demo-profesora', 'profesora@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Camila', 'Rojas');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('6b1f5301-840d-4261-a9ff-45c5e9e0e64c', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'profesora@demo.oppytalent.com',
                'Camila Rojas Vergara', 'Profesora de Biología y Ciencias Naturales', 'Persona proactiva y responsable, capaz de realizar distintas tareas de forma autónoma y eficiente. Con gran habilidad comunicativa y disposición a aprender, comprometiendo valores y autocrítica. Ha desarrollado competencias importantes para la enseñanza y el aprendizaje en la actualidad, tal como el aprendizaje basado en proyecto, la aplicación de estrategias didácticas basadas en las neurociencias y en las habilidades científicas.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/generic_avatar.webp', '+56 9 888 55 333', 'https://www.linkedin.com/in/demo02',
                NULL, NULL, 'Rancagua, Chile',
                '[]', '[]',
                '["Proactividad", "Responsabilidad", "Autonom\u00eda", "Eficiencia", "Habilidad comunicativa", "Disposici\u00f3n a aprender", "Autocr\u00edtica", "Ense\u00f1anza", "Aprendizaje basado en proyectos", "Estrategias did\u00e1cticas basadas en neurociencias", "Habilidades cient\u00edficas"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('3e3f948b-7de8-4d67-af99-07ed6783fbbc', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Liceo Polivalente Las Araucarias', 'Profesora de Biología',
                    '2025-01-01', NULL, 'Experiencia extraída',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('70de061e-dd0f-4cb7-9ab4-36297153fb8e', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Colegio Cumbres del Maipo', 'Profesora de Biología y Ciencias Naturales',
                    '2024-01-01', NULL, 'Experiencia extraída',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('759c5a64-ed8c-4ad6-bf88-be7d758d311e', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Colegio Andes de Maipú', 'Profesora de Biología y Ciencias Naturales',
                    '2023-01-01', NULL, 'Experiencia extraída',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5c044575-ee3c-403e-b968-83ff74fa5b26', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Colegio San Ignacio de Loyola', 'Profesora de Biología y Ciencias Naturales',
                    '2018-01-01', '2022-12-01', 'Experiencia extraída',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('c5d3ce08-118e-4832-9e90-3dc79de31677', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Colegio Santa Teresita del Niño Jesús', 'Profesora de Biología y Ciencias Naturales',
                    '2016-01-01', '2017-12-01', 'Trabajo en asignatura de innovación "Proyecto" junto con el Programa de Iniciativas Científicas Escolares (PICE) del Centro de Biociencias Aplicadas en los niveles de III y IV medio.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('7c1ab52d-bc74-4b9b-830c-615a0cc35b5e', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Universidad Austral de Pedagogía', 'Licenciada en Educación en Biología y Pedagogía en Biología con mención en Ciencias Naturales, Profesora de Biología y Ciencias Naturales',
                    2015, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('bdd706e9-471f-4ae6-b65e-d467044803da', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Liceo Bicentenario Santa María', 'Educación Media',
                    2005, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('34eb601d-a3f0-4ee8-8b26-1d15e539726a', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Colegio San Patricio de Las Condes', 'Educación Básica',
                    1999, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('db1df2fe-e4c4-406a-937d-fb56d5e11abf', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Centro de Investigación Biomédica Austral', 'Curso Biología Molecular y genómica – Fundación Científica Bios',
                    2016, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('3a2f3ca7-0b92-4b15-b932-b249f15c67bc', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Centro de Investigación Biomédica Austral', 'Curso Biología Microbiología – Fundación Científica Bios',
                    2017, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('08e9d9a8-a1df-4fc4-8c93-7bc823f8658a', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Instituto de Desarrollo Docente Futuro', 'Diseño De ABP Para El Desarrollo De Competencias Del XXI',
                    2021, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('790dece6-8417-45d1-96eb-664f2c9d4133', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Academia de Neurociencias Educativas', 'Diplomado en Neurociencia y Educación Basada en Evidencia',
                    2024, 'Estudio extraído', NULL, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('7a8b485c-86ce-40e3-ab94-9b76fecab4d1', '7dc9349c-dea5-40bb-8e1d-3d56599ef60d', 'Asignatura de innovación ''Proyecto'' con el Programa de Iniciativas Científicas Escolares del Centro de Biociencias Aplicadas', 'Trabajo en asignatura de innovación ''Proyecto'' junto con el Programa de Iniciativas Científicas Escolares (PICE) del Centro de Biociencias Aplicadas en los niveles de III y IV medio.',
                    'Trabajo en asignatura de innovación ''Proyecto'' junto con el Programa de Iniciativas Científicas Escolares (PICE) del Centro de Biociencias Aplicadas en los niveles de III y IV medio.', '["Innovaci\u00f3n educativa", "Colaboraci\u00f3n", "Dise\u00f1o curricular"]',
                    'null', '["Innovaci\u00f3n educativa", "Colaboraci\u00f3n", "Dise\u00f1o curricular"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-mecanico';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'demo-mecanico', 'mecanico@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Marcelo', 'Rojas');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('78023a54-bac0-441a-a977-8e8341e8ad91', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'mecanico@demo.oppytalent.com',
                'Marcelo Andrés ROJAS', 'Mecánico, Mantenimiento y Soldador Especializado', 'Con +10 años de experiencia como soldador especializado, y herrero y +5 años trabajando como mecánico de mantenimiento para maquinaria pesada. He llevado a cabo proyectos de gran envergadura como perforaciones para molinos, trabajos para parques industriales, ferrocarriles, construcción y reparación de tanques para hidrocarburos, entre otros. Me he desempeñado como oficial especializado de mantenimiento del sector de Herrería para la empresa Ingeniería Austral y como Supervisor de Cierre Final en tanques y calderas de hidrocarburo para la empresa Montajes Cordillera, manejando equipos multidisciplinares conformados por más de 10 oficiales mecánicos, electricistas, soldadores certificados y amoladores. Actualmente busco nuevas oportunidades laborales que me permitan continuar con mi desarrollo personal y profesional aportando todos mis conocimientos y habilidades profesionales para dirigir equipos de trabajo en obras o, realizar funciones operativas como operador ya sea en sectores de la minería, petróleo o construcción',
                'https://example.com/anon-avatar.webp', '+56 9 555 55 555', 'https://www.linkedin.com/in/demo03',
                NULL, NULL, 'Concepción, Chile',
                '[]', '[]',
                '["Organizaci\u00f3n y Planificaci\u00f3n", "Dotes comunicacionales", "Gesti\u00f3n del tiempo", "Toma de decisiones", "Orientaci\u00f3n al resultado", "Trabajo en equipo", "Adaptabilidad", "Capacidad para trabajar bajo presi\u00f3n", "Liderazgo", "Resoluci\u00f3n de conflictos", "Capacidad para delegar", "Toma de riesgos", "Motivaci\u00f3n para el logro", "Detallista", "Orientado a la seguridad", "Conocimiento de seguridad higiene en yacimientos"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('08477d34-61f6-47e6-8741-3284b7aac45d', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Soluciones Industriales del Desierto S.A.', 'OFICIAL ESPECIALIZADO/OPERADOR DE GRÚA TELESCÓPICA',
                    '2022-06-01', NULL, 'Ejecución de mantenimiento preventivo, predictivo y correctivo en sistemas mecánicos y electromecánicos dentro de la planta.
Intervenciones en cintas transportadoras, tambores motrices y de cola, y elevadores de cangilones, incluyendo alineación, cambio de rodamientos y montaje con grúa telescópica de hasta 63.503 kg.
Montaje completo de elevadores de cangilones, con puesta en marcha y ajuste final en campo. Mantenimiento integral de compresores industriales (Atlas Copco, Sullair, Setec) y compresores GNC, incluyendo limpieza de filtros, verificación de presiones, lubricación y reemplazo de válvulas. Mantenimiento en generadores Caterpillar a GNC, abarcando: Revisión de componentes eléctricos (cableado, alternadores, tableros de control). Diagnóstico y recambio de sensores (temperatura, presión, oxígeno, knock, MAP, entre otros). Ejecución de servicios programados: cambio de filtros, lubricación, ajuste de válvulas, inspección de bujías y verificación de parámetros de funcionamiento. Detección de fallas relacionadas a inyección, encendido y funcionamiento del motor por medios manuales y mediante escáner. Coordinación con áreas de seguridad, electricidad e instrumentación durante paradas y arranques de planta.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('414754c0-a7d1-4579-adca-cf8c9fb30829', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Mantenimiento Proactivo Minero Ltda.', 'OFICIAL ESPECIALIZADO EN MANTENIMIENTO MECÁNICO',
                    '2021-01-01', '2022-06-01', 'Mantenimiento preventivo y correctivo de flota pesada y liviana, equipos viales, y maquinaria de planta. Servicio y diagnóstico en generadores Caterpillar a GNC. Intervención en horno de secado: alineación, control de temperatura y mantenimiento de rodillos. Tareas de montaje, inspección y ajuste de cintas transportadoras y estructuras móviles. Aplicación de protocolos de seguridad, medioambiente y calidad en las tareas críticas.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('446b3bb9-45f7-40b6-ade1-d35a5d3969b4', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Exploraciones Geomin S.p.A.', 'MOTORISTA DE EQUIPO DE PERFORACIÓN',
                    '2019-12-01', '2020-05-01', 'Montaje de equipo de perforación con VFD, HPU, circuito neumático e hidráulico. Mantenimiento en equipo RIG Pace 900 y equipos F mesa rotari, dravuor, TM 80, ST 80, GUINCH., corona, bombas de lodo, catwol. Reparación de freno en cuadro de maniobra, top drive (lower, griper, -vacap, torbus,rotari). Servicio y reparación de DTM (desmontaje traslado y montaje) en equipos 900,990, y F 10,F 07 , F 24.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('1c709c22-9c48-4e47-ae00-54856fcc9081', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Equipos Pesados del Sur S.A.', 'TÉCNICO MECÁNICO',
                    '2019-02-01', '2019-11-01', 'Mantenimiento mecánico y preventivo de equipos pesado y soldador para empresas como: Caterpillar, Komatsu, Volvo, zanjadora tesmec y trencor, curvadoras. Herrería: fabricación reconstrucción de balde, retro pala mantenimiento en cadena de corte de sanjandora (placa de rebote, fabricación de bolsillo, cambio de porta pica contacto).',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('685baef3-abf2-42f2-9f4c-6b3d07a830a3', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Estructuras y Montajes Andinos Ltda.', 'SUPERVISOR EN MONTAJE MECÁNICO',
                    '2018-01-01', '2019-01-01', 'Soldador especializado en tanques y caldera para hidrocarburo. A cargo de supervisar el cierre final en batería',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('3356a80b-acce-49e4-acab-d2dd2f283f30', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Ingeniería y Construcción Patagónica S.A.', 'OFICIAL ESPECIALIZADO HERRERO Y SOLDADOR',
                    '2016-01-01', '2019-01-01', 'Mantenimiento en equipos pesado trencor, tesmec, lanzadores excéntrico y concéntrico, baldes, palas, cilindros, radiadores, etc.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('c4e11a77-8f63-4d11-8d78-593f4e6bb02a', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Taller Metalúrgico El Pionero', 'SOLDADOR',
                    '2015-01-01', '2016-01-01', 'Soldaduras de container, hidrogrúas, anclas, piletas, entre otras maquinarias, mediante procedimientos SMAW. Biselado en cañerías.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d47bc7c2-3bb7-471e-8ce1-fc1a4f60e326', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Liceo Técnico Industrial del Norte', 'Perito Mercantil',
                    2003, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('14bbf158-0434-4744-a119-bdd566f334f3', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Instituto Técnico Profesional Minero', 'Operación segura en equipos de izajes en: grúa movil hasta 63503kg',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('c38d2152-84d2-4eb8-85db-50f7db7df29b', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Centro de Formación Técnica El Desierto', 'Asistente en Recursos Petroleros',
                    2020, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('9b5a8ea9-b6aa-4fb2-a880-1a430191c3b8', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Academia de Capacitación Industrial Austral', 'Seguridad e Hígiene en Ambiente Laboral, Soldador y Oxicortador, Supervisor de Operaciones',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('f97ad58b-f91b-4b8f-b532-a91ac190a902', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Escuela Técnica de Operadores de Maquinaria', 'Curso Hidrogrúa Manejo Defensivo',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('567112ac-a5f7-4158-8225-e38c82c4e832', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Licencia de Conducir', 'E1 (camión con acoplado y/o articulado)',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('18d335c2-992d-488a-928d-97b583429557', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Licencia de Conducir', 'B1',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('99e88924-8fb4-40c8-89f6-a963e210ad92', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Licencia de Conducir', 'C',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('2af0f453-44cf-4f91-99df-c340cf26d488', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Licencia de Conducir', 'E2 (maquinarias especiales no agrícolas)',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('5af7d7a2-4b8e-449e-a72d-33b59dfe156e', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Licencia de Conducir', 'A2 (motocicletas mas de 150 CC a 300 cc)',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('4ad4727f-eaf2-44ec-a014-f06701c7d1a3', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Disponibilidad', 'Disponibilidad para radicarse en otro lugar',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('665a83bd-d060-41f7-9ce6-0d8e9a052031', '4fcdaf31-7140-4b89-b665-0fb236a2a1aa', 'Disponibilidad', 'Disponibilidad para viajar',
                    'Detalle de la habilitación', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-comunicadora';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('2b273217-cdd0-4366-8f32-bc502a285643', 'demo-comunicadora', 'comunicadora@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Valeria', 'Contreras');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('b7a4299b-40ee-4651-8def-b194eb1801d2', '2b273217-cdd0-4366-8f32-bc502a285643', 'comunicadora@demo.oppytalent.com',
                'Valeria Contreras Soto', 'LIC. EN COMUNICACIÓN, CON ESPECIALIDAD EN PUBLICIDAD Y MARKETING', 'Me defino por ser una persona proactiva, que aprende rápido, con ganas de crecer y ser parte de la mejor empresa.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/placeholder-avatar.webp', '+56 9 888 55 333', 'https://www.linkedin.com/in/demo04',
                NULL, NULL, 'Puerto Montt, Chile',
                '[]', '[]',
                '["Event Planner", "Comunicaci\u00f3n", "Business Strategist", "Relaciones P\u00fablicas", "Customer Service", "Experiencias", "Publicidad", "Marketing", "Expos y Congresos", "Eficiencia", "Liderazgo", "Proactividad", "Comunicaci\u00f3n asertiva", "Gesti\u00f3n del tiempo", "Trabajo en equipo", "Tolerancia a la frustraci\u00f3n", "Adaptabilidad al cambio", "Ingl\u00e9s C1", "Canva", "Slack", "Teams", "Monday", "Microsoft 360", "Locuci\u00f3n", "Office"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('c40337d7-c12a-4620-9a06-a2540407ab58', '2b273217-cdd0-4366-8f32-bc502a285643', 'Visión Estratégica SpA', 'Relaciones Públicas',
                    '2018-01-01', '2019-01-01', 'Atención a clientes, seguimiento a clientes. Participación en ferias y eventos. Desarrollo de la comunicación de los diferentes giros de la empresa. Búsqueda de promocionales y relación con clientes nuevos y existentes.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('e788e700-156a-490b-b481-2f7e92a9e502', '2b273217-cdd0-4366-8f32-bc502a285643', 'Grupo Impulso Sur', 'Gerente de Comunicación, Mkt y Relaciones Públicas',
                    '2023-03-01', '2023-10-01', 'Desarrollo del área de comunicación (supervisión página, videos institucionales, creación flyers, tarjetas de productos, presentaciones, minutas, etc). Búsqueda de espacios para patrocinar eventos deportivos y tener presencia de marca. Desarrollo de la comunicación de los diferentes giros de la empresa. Búsqueda de promocionales y relación con clientes nuevos y existentes.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('d43db459-c7c9-44d7-ad6c-2fc30dc2de54', '2b273217-cdd0-4366-8f32-bc502a285643', 'Patagonia Capital Holding', 'Gerente de Comunicación y Relaciones Públicas',
                    '2020-10-01', '2022-05-01', 'Desarrollo de estrategias de comunicación de productos y servicios (creación de brochures, presentaciones, invitaciones, trípticos, minutas, etc). Planificación de las actividades de comunicación y marketing. Realización de eventos para los productos o servicios de nuestros clientes. Encargada de las relaciones públicas y atención a clientes.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('e6693bd3-08f0-4ecc-8820-43529e99c0bd', '2b273217-cdd0-4366-8f32-bc502a285643', 'Branding Élite Solutions', 'Key Account Manager',
                    '2019-12-01', '2020-07-01', 'Atender los pitches de las diferentes marcas, bajar la información con el equipo y hacer propuestas para cada una de las necesidades de los clientes. Organización de eventos, creación junto con el equipo de diseño de stands, lanzamientos de marca y experiencias para Viña del Maipo, Destilería Austral, Grupo Élite, Panadería La Espiga, Medios del Sur, etc. Generación de estrategias especiales de comunicación para sus productos y/o servicios. Búsqueda de venues, selección de catering, selección de promocionales, seguimiento a clientes, presentaciones, minutas.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('a1a4725c-d228-47e1-a39e-6a0038fd977b', '2b273217-cdd0-4366-8f32-bc502a285643', 'Eventos Cima', 'Gerente de Comunicación, Mkt y Relaciones Públicas',
                    '2019-02-01', '2019-12-01', 'Briefing de clientes. Especialización en atención a clientes y seguimiento. Búsqueda de proveedores, creación de cotizaciones, búsqueda de venues, artículos promocionales, selección de catering, scouting, materiales pop. Coordinación de eventos, coordinación de promotoras, activaciones, conciertos, campañas, producción y desarrollo de estrategias de comunicación y planeación.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('ac64b076-6573-4492-959d-0e066040744a', '2b273217-cdd0-4366-8f32-bc502a285643', 'UNIVERSIDAD ANDES COMUNICACIÓN Y MEDIOS', 'LIC. EN COMUNICACIÓN, CON ESPECIALIDAD EN PUBLICIDAD Y MARKETING',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('8c582676-7b47-4d89-8149-9d8df9667bbd', '2b273217-cdd0-4366-8f32-bc502a285643', 'Coordinadora - ImpulsaMarketing', 'Supervisión de los videos de la empresa. Creación de preguntas para los invitados y seguimiento a los mismos. Atención a expertos en rh y clientes. Atención y respuesta a los comentarios de los participantes durante las transmisiones de las entrevistas a expertos en rh.',
                    'Supervisión de los videos de la empresa. Creación de preguntas para los invitados y seguimiento a los mismos. Atención a expertos en rh y clientes. Atención y respuesta a los comentarios de los participantes durante las transmisiones de las entrevistas a expertos en rh.', '["Coordinaci\u00f3n", "Gesti\u00f3n de contenido", "Atenci\u00f3n al cliente", "Gesti\u00f3n de transmisiones"]',
                    'null', '["Coordinaci\u00f3n", "Gesti\u00f3n de contenido", "Atenci\u00f3n al cliente", "Gesti\u00f3n de transmisiones"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('39772873-b048-4cda-9189-6fbed648447d', '2b273217-cdd0-4366-8f32-bc502a285643', 'Logística - Universidad del Maule', 'Realización de los eventos que organizó la Universidad junto con la Fundación Horizonte Latinoamericano.',
                    'Realización de los eventos que organizó la Universidad junto con la Fundación Horizonte Latinoamericano.', '["Log\u00edstica de eventos", "Organizaci\u00f3n de eventos"]',
                    'null', '["Log\u00edstica de eventos", "Organizaci\u00f3n de eventos"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('bafd6892-940b-4191-8d39-4b1dbcc787e2', '2b273217-cdd0-4366-8f32-bc502a285643', 'Logística - Evento Deportivo ''Copa Cóndor''', 'Acreditación a los medios de comunicación masivos para el juego, envió de invitaciones y comunicación constante con ellos.',
                    'Acreditación a los medios de comunicación masivos para el juego, envió de invitaciones y comunicación constante con ellos.', '["Log\u00edstica", "Relaciones con medios"]',
                    'null', '["Log\u00edstica", "Relaciones con medios"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('d1e80710-bbbb-4b5c-9887-48c3951958ab', '2b273217-cdd0-4366-8f32-bc502a285643', 'Locución para Medios Digitales', 'Radio Onda Digital, Ministerio de Desarrollo Social. Desarrollo de cápsulas comerciales digital/radio. Voz en OFF para una campaña nacional.',
                    'Radio Onda Digital, Ministerio de Desarrollo Social. Desarrollo de cápsulas comerciales digital/radio. Voz en OFF para una campaña nacional.', '["Locuci\u00f3n", "Producci\u00f3n de audio"]',
                    'null', '["Locuci\u00f3n", "Producci\u00f3n de audio"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('75f4c50d-eed1-468a-abb0-b24e0c77a999', '2b273217-cdd0-4366-8f32-bc502a285643', 'Proyectos Independientes 2026', 'Traducción del español al inglés para un grupo de 15 personas polacas. Traducción del español al inglés para un grupo de 10 personas Turcas. Coordinación del valet parking de un estacionamiento privado para una serie de eventos.',
                    'Traducción del español al inglés para un grupo de 15 personas polacas. Traducción del español al inglés para un grupo de 10 personas Turcas. Coordinación del valet parking de un estacionamiento privado para una serie de eventos.', '["Traducci\u00f3n", "Coordinaci\u00f3n", "Log\u00edstica"]',
                    'null', '["Traducci\u00f3n", "Coordinaci\u00f3n", "Log\u00edstica"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('f0e28f4f-f113-49ae-b7b6-944b460e8a35', '2b273217-cdd0-4366-8f32-bc502a285643', 'Proyectos Independientes 2024/2025 - Producción', 'Responsable de la operación del evento. Supervisión del staff, registro y montaje. Resolución de problemas. Coordinación de catering y barra para diferentes eventos en Santiago, Valparaíso, y Concepción. Coordinación de edecanes, y meseros, para cubrir todas las necesidades del evento. Trato con proveedores, búsqueda de artículos y servicios para el evento y cotizaciones. Relaciones Públicas (NO VENTAS). Trato y seguimiento con clientes. Logística de transporte y vuelos.',
                    'Responsable de la operación del evento. Supervisión del staff, registro y montaje. Resolución de problemas. Coordinación de catering y barra para diferentes eventos en Santiago, Valparaíso, y Concepción. Coordinación de edecanes, y meseros, para cubrir todas las necesidades del evento. Trato con proveedores, búsqueda de artículos y servicios para el evento y cotizaciones. Relaciones Públicas (NO VENTAS). Trato y seguimiento con clientes. Logística de transporte y vuelos.', '["Producci\u00f3n de eventos", "Gesti\u00f3n de staff", "Gesti\u00f3n de catering", "Relaciones P\u00fablicas", "Gesti\u00f3n de proveedores", "Log\u00edstica"]',
                    'null', '["Producci\u00f3n de eventos", "Gesti\u00f3n de staff", "Gesti\u00f3n de catering", "Relaciones P\u00fablicas", "Gesti\u00f3n de proveedores", "Log\u00edstica"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('912583c2-8595-4178-a601-230414ec87ae', '2b273217-cdd0-4366-8f32-bc502a285643', 'Business Strategist - Pulsar Capital', 'Desarrollo e implementación de estrategias para alcance de objetivos. Estrategia OFF para lanzamiento (cotizaciones, proveedores, merch etc.). Análisis del mercado, competencia y procesos internos. Relaciones Públicas (no ventas).',
                    'Desarrollo e implementación de estrategias para alcance de objetivos. Estrategia OFF para lanzamiento (cotizaciones, proveedores, merch etc.). Análisis del mercado, competencia y procesos internos. Relaciones Públicas (no ventas).', '["Business Strategy", "An\u00e1lisis de mercado", "Relaciones P\u00fablicas"]',
                    'null', '["Business Strategy", "An\u00e1lisis de mercado", "Relaciones P\u00fablicas"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('fe2566fd-605a-4666-841f-ce363c3bd1e7', '2b273217-cdd0-4366-8f32-bc502a285643', 'Producción - Agencia Estelar', 'Selección de talentos. Contacto con los talentos. Coordinar audiciones. Seguimiento.',
                    'Selección de talentos. Contacto con los talentos. Coordinar audiciones. Seguimiento.', '["Producci\u00f3n", "Gesti\u00f3n de talento", "Coordinaci\u00f3n de audiciones"]',
                    'null', '["Producci\u00f3n", "Gesti\u00f3n de talento", "Coordinaci\u00f3n de audiciones"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('f4495ef5-3cd8-4951-82e0-6635ce652c83', '2b273217-cdd0-4366-8f32-bc502a285643', 'Asistente de Talento - Certamen Internacional de Belleza ''Estrella del Pacífico''', 'Encargada de la agenda personal de 6 figuras de belleza internacionales. Logística. Organización de actividades. Resolución de problemas. Producción.',
                    'Encargada de la agenda personal de 6 figuras de belleza internacionales. Logística. Organización de actividades. Resolución de problemas. Producción.', '["Asistencia de talento", "Log\u00edstica", "Organizaci\u00f3n de eventos", "Producci\u00f3n"]',
                    'null', '["Asistencia de talento", "Log\u00edstica", "Organizaci\u00f3n de eventos", "Producci\u00f3n"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('f0c6129f-3f0c-4447-ae32-d9aaced5078c', '2b273217-cdd0-4366-8f32-bc502a285643', 'Asistente de Dirección - Consultora Horizonte', 'Encargada del contacto con los clientes y seguimiento a prospectos. Apoyo al área administrativa y comercial. Control de candidatos y cuentas.',
                    'Encargada del contacto con los clientes y seguimiento a prospectos. Apoyo al área administrativa y comercial. Control de candidatos y cuentas.', '["Asistencia administrativa", "Gesti\u00f3n de clientes", "Gesti\u00f3n de candidatos"]',
                    'null', '["Asistencia administrativa", "Gesti\u00f3n de clientes", "Gesti\u00f3n de candidatos"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('89d23c2e-013b-4313-8e3c-1fa142af5b00', '2b273217-cdd0-4366-8f32-bc502a285643', 'Coordinadora - Cumbres Globales', 'Trato y seguimiento con clientes. Creación de presentaciones y dinámicas, selección de giveaways y materiales para las conferencias. Acompañamiento a conferencias y asistencia durante todo el evento.',
                    'Trato y seguimiento con clientes. Creación de presentaciones y dinámicas, selección de giveaways y materiales para las conferencias. Acompañamiento a conferencias y asistencia durante todo el evento.', '["Coordinaci\u00f3n de eventos", "Gesti\u00f3n de clientes", "Creaci\u00f3n de presentaciones"]',
                    'null', '["Coordinaci\u00f3n de eventos", "Gesti\u00f3n de clientes", "Creaci\u00f3n de presentaciones"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-contadorauditor';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('7c81c8c7-cce1-4452-8fcc-081c7977702d', 'demo-contadorauditor', 'contadorauditor@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Javier', 'Fuentes Morales');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('517a749f-33f0-4286-ab2b-a26438672da3', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'contadorauditor@demo.oppytalent.com',
                'JAVIER FUENTES MORALES', 'Contador Auditor | Finanzas, RRHH y control de gestión | Especialista en tesorería y administración', 'Contador Auditor con destacada experiencia liderando áreas contables, financieras, administrativas y de recursos humanos en empresas de diversos sectores. Me especializo en la elaboración de estados financieros, control de gestión, planificación presupuestaria, etc. A lo largo de mi trayectoria, he gestionado con éxito los requerimientos de las gerencias y dueños en implementación de sistemas ERP, modernización administrativa y optimización de recursos. Destaco por mi dominio de herramientas como Microsoft Excel, así como de sistemas ERP como Softland, Defontana, Flexline y Payroll. Me caracteriza un enfoque práctico, orientado a resultados, y la capacidad de alinear la gestión financiera con los objetivos estratégicos del negocio.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/de2cabbe1c814d5480186d2aa747831b_Richard-Avatar.webp', '+56 9 555 123 456', 'https://www.linkedin.com/in/demo05',
                NULL, NULL, 'La Serena, Chile',
                '[]', '[]',
                '["Microsoft Excel", "Softland", "Defontana", "Flexline", "Payroll", "ERP", "Contabilidad", "Finanzas", "Administraci\u00f3n", "Recursos Humanos", "Control de gesti\u00f3n", "Planificaci\u00f3n presupuestaria", "Tesorer\u00eda", "Liderazgo", "Toma de decisiones", "An\u00e1lisis financiero", "Gesti\u00f3n de costos", "Facturaci\u00f3n electr\u00f3nica", "Auditor\u00eda interna", "Negociaci\u00f3n con proveedores", "Procesos de licitaci\u00f3n p\u00fablica", "Power BI", "ERP Manager"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('45daa430-7bac-4606-a08f-f265292170b9', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Independiente', 'Asesor Contable',
                    '2023-01-01', NULL, '- Prestación de asesorías contables, financieras y tributarias a microempresas, PYMES y emprendedores.
- Apoyo en la implementación y manejo de sistemas ERP para control contable y de remuneraciones.
- Elaboración de declaraciones de renta, balances, estados financieros y reportes para fines bancarios o comerciales.
- Acompañamiento en procesos de formalización de empresas, estructuración financiera y optimización de costos.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('d8569b5b-10bc-4982-a4f4-e29c97a60349', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'ControlMax SpA', 'Encargado de Activo Fijo y Control de Gestión',
                    '2022-01-01', '2024-01-01', '- Gestión integral del activo fijo, incluyendo la valorización, registro contable, control de incorporaciones, bajas y depreciaciones, conforme a la normativa vigente.
- Preparación de cierres contables mensuales, generación de balances e informes financieros, en coordinación con el área contable y la gerencia.
- Análisis detallado de cuentas de gastos, detección de desviaciones presupuestarias y propuesta de ajustes para optimizar la asignación de recursos.
- Elaboración de informes de control de gestión con foco en costos, márgenes y desempeño financiero, apoyando la toma de decisiones estratégicas.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('24ef61dc-63f2-4d53-98df-b2c9621b1416', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Salud Integral S.A.', 'Jefe de Administración y Finanzas',
                    '2015-01-01', '2020-01-01', '- Supervisión general de las áreas contable, financiera, administrativa y de recursos humanos, asegurando el cumplimiento de políticas internas y normativas legales.
- Elaboración de estados financieros, balances mensuales e informes de gestión, incluyendo análisis de costos, ventas, rentabilidad, factor margen y flujo de caja semanal.
- Operación y administración del ERP Softland en módulos de contabilidad, inventario, producción, cuentas corrientes, clientes, proveedores, recursos humanos y compras, utilizando el generador de informes como herramienta de gestión.
- Formulación de presupuestos semestrales, control de costos y análisis mensual contable-financiero para evaluar el desempeño económico de la empresa.
- Logros destacados:
    - Organicé el proceso de compras y optimicé los procedimientos administrativos, lo que permitió mejorar la eficiencia operativa y reducir significativamente los tiempos de respuesta.
    - Implementé la facturación electrónica, lo que contribuyó a modernizar los procesos comerciales y a aumentar la eficiencia en la gestión de ventas y cobranzas.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('d1c73b03-4d6d-45a3-907e-79ca6425f9b0', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Fundación Educacional Futuro', 'Jefe de Administración, Finanzas y RRHH',
                    '2011-01-01', '2015-01-01', '- Dirección de los procesos administrativos, financieros y de recursos humanos, incluyendo la planificación, control y organización del área y sus equipos.
- Gestión de recursos humanos, abarcando selección de personal, compensaciones, contratación, finiquitos, liquidaciones de sueldo, desarrollo organizacional y procesos de capacitación.
- Elaboración y control del presupuesto anual, confección de estados financieros, realización de auditorías internas e informes de gestión para el directorio.
- Coordinación de procesos de licitación pública, participación en Convenios Marco y gestión a través de la plataforma ChileProveedores.
- Administración de compras generales, negociaciones con proveedores y control de abastecimiento institucional.
    - Logros destacados:
        - Implementé el sistema ERP Defontana en las áreas de recursos humanos, tesorería y ventas, lo que permitió integrar procesos clave, mejorar la trazabilidad de la información y optimizar la gestión administrativa de la empresa.
        - Diseñé e implementé políticas internas y lideré la apertura de nuevas unidades funcionales, fortaleciendo la estructura organizacional y facilitando el crecimiento operativo de la empresa.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('7f2bf7ad-5132-4e80-926b-d3cdb82c630f', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Desarrollos Inmobiliarios Cordillera', 'Encargado de Administración y Finanzas',
                    '2003-01-01', '2011-01-01', '- Supervisión de las áreas de finanzas y personal, con más de 50 trabajadores a cargo.
- Coordinación de contabilidad, balances, estados financieros, pagos y conciliaciones bancarias.
- Gestión de compras, control de flujos de caja y relación con proveedores.
- Elaboración y control presupuestario, licitaciones públicas y auditorías internas.
- Administración de procesos de RRHH: selección, contratos, liquidaciones y finiquitos.
    - Logros destacados:
        - Ordené el funcionamiento administrativo y financiero mediante la implementación de normas y procedimientos, junto con canales de comunicación más eficientes, lo que permitió profesionalizar la gestión del área.
        - Implementé sistemas de control en los procesos de tesorería y finanzas, fortaleciendo la trazabilidad y la transparencia en la gestión financiera.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('5305ea14-d7da-4f5c-9015-be221bfa963c', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Universidad del Pacífico Austral', 'Contador Auditor',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d364a30a-4311-4d5f-a009-c799266acd8f', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Instituto Profesional Andes', 'Contador General',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d44f5a15-68c4-4638-aee4-5d9cdcf2890b', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Academia Financiera Australis', 'Finanzas Corporativas',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('4eff0cf4-3557-44d2-8cab-2fdc4d82493c', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Centro de Capacitación Empresarial Capital', 'Planificación y estructura de empresas (EIRL)',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('f12f8a2a-da54-40f5-beed-cdd00f4899a4', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Editorial Jurídica del Sur', 'Declaraciones Anuales Impuesto a la Renta',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('ccd2486d-6ff6-4612-be64-46711a6fc4f9', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Editorial Jurídica del Sur', 'Instrucciones para la emisión de Certificados y Declaraciones',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('b99475fc-f958-44d1-ba11-03deb6a37678', '7c81c8c7-cce1-4452-8fcc-081c7977702d', 'Licencia', 'Licencia de conducir Clase B',
                    'Detalle de la habilitación', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-arquitecto';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'demo-arquitecto', 'arquitecto@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Matías', 'González');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('08c67451-f876-454e-b2e9-f142a14d147e', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'arquitecto@demo.oppytalent.com',
                'Matías González Fuentes', 'Arquitecto', 'Arquitecto con tres años de experiencia en proyectos de ámbito urbanístico y paisajístico, con gran énfasis e interés por el diseño arquitectónico y urbano desde una mirada integral. He colaborado en proyectos de diversas escalas y temáticas, destacando por mi compromiso, entrega e innovación en las diferentes instancias del desarrollo arquitectónico. Cuento con patente profesional vigente.',
                'https://demo.oppytalent.com/avatar_placeholder.webp', '+56 9 888 55 333', 'https://www.linkedin.com/in/demo06',
                NULL, NULL, 'Iquique, Chile',
                '[]', '[]',
                '["AutoCAD", "Revit", "Navisworks", "Photoshop", "Unreal Engine", "Proyectos de Arquitectura", "Dise\u00f1o Urbano", "Paisajismo", "Modelado BIM", "Accesibilidad Universal"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('ee6243ab-365e-4028-bf81-c4bb59fc37f5', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Paisajes Urbanos Consultores', 'Arquitecto Paisajista Junior',
                    '2024-01-01', '2025-10-01', '- Me he desempeñado como Arquitecto junior en Diseño Urbano, confeccionando planimetrías, detalles, soluciones arquitectónicas y paisajísticas para diversos proyectos a lo largo del país, donde destacan Paseo Fluvial Biobío, Acceso Costero Pucón, Conexión Vial Rancagua, Ribera Parque Metropolitano, Renovación Urbana La Pintana, Concesión Vial Ruta del Maule, entre otros, obteniendo diseños base para su posterior desarrollo.
- Desarrollé la especialidad de Paisajismo en modelos BIM para proyecto de vialidad MOP en Rancagua, contribuyendo a un modelo federado con las diversas especialidades necesarias para completar el proyecto en la plataforma Trimble.
- He trabajado en el desarrollo de proyectos de Accesibilidad Universal en espacios públicos (Conexión Vial Rancagua, Ruta E-85, Paseo Costanera Copiapó, Mejoramiento espacio público Sector Ribera - Parque Metropolitano y Acceso Costero Pucón) logrando soluciones requeridas según estándares MINVU.
- Asimismo, también desarrollé material gráfico de apoyo (modelos 3D, renders, presentaciones) para complementar la propuesta técnica de cada proyecto.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('1f9490a6-8730-48e0-b280-06bd9999a4c4', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Profesional Autónomo de Arquitectura', 'Desarrollo de proyectos de pequeña – mediana escala',
                    '2020-03-01', NULL, '- Ha regularizado y tramitado permisos de edificación y recepción final en ampliaciones de viviendas sociales u otras edificaciones similares.
- Participé en concursos de Arquitectura, tanto públicos como privados de forma independiente y asociada con otros arquitectos. También he desarrollado propuestas de anteproyecto con fines particulares.
- He tenido colaboraciones puntuales para la edición, fotografía e imagen de un texto académico en proceso de publicación. Actualmente me dedico de manera aficionada a la fotografía de arquitectura.
- He desarrollado diversos modelos 3D y BIM para posterior renderizado y producción gráfica como apoyo a entes u oficinas particulares, así como también presentaciones y video recorridos interactivos en 3D.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('ec305068-c5a7-4a22-ad7b-277286043467', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Universidad Central de Santiago', 'Arquitectura – Título Profesional de Arquitecto',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('81e9a96a-2aed-43a1-b642-41b12e494ec5', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Universidad Central de Santiago', 'Arquitectura – Licenciado en Arquitectura',
                    2019, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('a31c4215-0dd0-4d5c-a8f6-7046dc7e5d6c', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Universidad Central de Santiago', 'Diplomado BIM para modelado, gestión, documentación y coordinación MEP.',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('7c73fa61-c38e-44ee-862c-de442ef81a05', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Instituto Chileno de Innovación en Construcción – Programa BIM Avanzado', 'Introducción a estándares y tecnologías BIM',
                    2022, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('5b26d5d2-ff0c-439d-8e28-223fbae66c72', '562cf7d6-82d5-42f5-8b7e-0b0657e9bebb', 'Universidad Central de Santiago', 'Diplomado en Tecnologías de la Construcción mención BIM',
                    2022, 'Estudio extraído', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-ingenierocivilenautomatizacion';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('ee90cef8-9b83-4689-ae35-4b036f84f780', 'demo-ingenierocivilenautomatizacion', 'ingenierocivilenautomatizacion@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Rodrigo', 'Acevedo');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('9da7fafb-d0ff-4e95-87dd-2504add84f19', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'ingenierocivilenautomatizacion@demo.oppytalent.com',
                'RODRIGO ALEJANDRO ACEVEDO SOTO', 'Ingeniero Civil en Automatización', 'Ingeniero Civil en Automatización con formación en control de procesos, instrumentación industrial y sistemas de control. Experiencia en integración de tableros eléctricos, pruebas punto a punto y levantamiento de datos en terreno. Manejo de PLC Siemens S7-1200 en TIA Portal, lógica Ladder y desarrollo básico de HMI. Conocimientos en programación (Python, C/C++), análisis de datos y aplicación de inteligencia artificial. Experiencia en desarrollo de herramientas basadas en modelos de lenguaje (LLMs) ejecutados localmente, incluyendo implementación de arquitecturas RAG (Retrieval-Augmented Generation) para procesamiento y traducción de texto con contexto semántico. Interés en automatización industrial, Industria 4.0, inteligencia artificial aplicada y desarrollo de soluciones tecnológicas.',
                NULL, '+56 9 555 55 555', 'https://www.linkedin.com/in/demo07',
                NULL, NULL, 'Arica, Chile',
                '[]', '[]',
                '["Automatizaci\u00f3n y control de procesos", "PLC (Ladder", "Siemens S7-1200", "TIA Portal)", "Programaci\u00f3n (Python", "C/C++", "C#)", "Instrumentaci\u00f3n industrial", "Integraci\u00f3n de tableros el\u00e9ctricos (TDA/TDF)", "HMI", "AutoCAD", "An\u00e1lisis de datos y dashboards", "Modelos de lenguaje (LLMs)", "Ollama", "Arquitecturas RAG (Retrieval-Augmented Generation)", "Bases de datos vectoriales (ChromaDB)", "Procesamiento de lenguaje natural (NLP)", "Prompt engineering", "Desarrollo de herramientas de IA local", "Ofim\u00e1tica", "Trabajo en equipo", "Comunicaci\u00f3n efectiva", "Resoluci\u00f3n de problemas", "Adaptabilidad", "Gesti\u00f3n de inventario y log\u00edstica", "Atenci\u00f3n al cliente", "Trabajo en terreno", "Levantamiento de informaci\u00f3n", "Organizaci\u00f3n y planificaci\u00f3n"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('a7f09e78-782e-4ea4-9f62-b87096ec7710', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Instituto Nacional de Estadísticas y Censos (INEC Chile)', 'Censista',
                    '2024-03-01', '2024-07-01', '- Realicé levantamiento y validación de datos mediante entrevistas presenciales y registro en plataforma digital oficial.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('ebf3860c-797a-43a4-ae31-436e7bb01b83', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Servicio de Medición Educacional (SEMED)', 'Examinador y Asistente de Aula',
                    '2025-10-01', '2025-11-01', '- Supervisé el desarrollo de evaluaciones estandarizadas y apoyé a estudiantes con necesidades especiales, asegurando cumplimiento de protocolos.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('7863d17f-e406-400f-a953-e7bcbbfb5d18', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Laboratorio de Inteligencia Artificial Aplicada - U. del Biobío', 'Práctica Profesional II',
                    '2023-03-01', '2023-04-01', '- Colaboré en análisis de imágenes para proyectos de visión artificial, incluyendo etiquetado de datos y apoyo en investigación aplicada.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('50c5c788-18ab-427c-9a6b-807dcf6ee6b5', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Supermercados El Cóndor', 'Repartidor, Reponedor y Bodeguero',
                    '2024-11-01', NULL, '- Gestioné distribución de mercadería entre sucursales, optimizando tiempos de entrega.
- Apoyé reposición en sala de ventas y mantuve orden y control de inventario en bodega.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('23ffed6b-06cc-4437-afc1-cf729c514535', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Soluciones Robóticas del Centro S.A.', 'Práctica Profesional I',
                    '2022-02-01', '2022-03-01', '- Apoyé desarrollo de ingeniería en automatización industrial, incluyendo integración de tableros (TDA/TDF), compras técnicas y pruebas punto a punto.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('86402106-7e6a-40b8-893c-d7ef79865bc9', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Universidad Tecnológica Austral', 'Ingeniería Civil en Automatización',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('bd713840-2e41-473e-a7a2-ccc6049e36e7', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Instituto de Innovación Digital Chile', 'Fundamentos del Análisis de Datos',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('c30e3531-39f2-4af4-b964-f77333e0161c', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Desarrollo de herramientas basadas en modelos de lenguaje (LLMs)', 'Experiencia en desarrollo de herramientas basadas en modelos de lenguaje (LLMs) ejecutados localmente, incluyendo implementación de arquitecturas RAG (Retrieval-Augmented Generation) para procesamiento y traducción de texto con contexto semántico.',
                    'Experiencia en desarrollo de herramientas basadas en modelos de lenguaje (LLMs) ejecutados localmente, incluyendo implementación de arquitecturas RAG (Retrieval-Augmented Generation) para procesamiento y traducción de texto con contexto semántico.', '["LLMs", "RAG", "Ollama", "ChromaDB", "Procesamiento de lenguaje natural (NLP)", "Prompt engineering", "Desarrollo de herramientas de IA local"]',
                    'null', '["LLMs", "RAG", "Ollama", "ChromaDB", "Procesamiento de lenguaje natural (NLP)", "Prompt engineering", "Desarrollo de herramientas de IA local"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('1ddb27fe-5f4c-41c0-ad1c-a62847301ba5', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Beca', 'Beca para formación en análisis de datos',
                    'Instituto de Innovación Digital Chile', '2026-06', 'Beca adjudicada para formación en análisis de datos, incluyendo manejo de datos, procesamiento y herramientas orientadas a la toma de decisiones.', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('0b53d010-0506-4d1e-9ea2-4eaecdae39e6', 'ee90cef8-9b83-4689-ae35-4b036f84f780', 'Licencia', 'Licencia de conducir clase B',
                    'Detalle de la habilitación', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-chefdepartida';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('d88b7322-f270-4105-9a35-0c318e2bab73', 'demo-chefdepartida', 'chefdepartida@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Antonia', 'Valenzuela');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('428bb1e8-82d7-4692-ab0b-74d07e7d2ae5', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'chefdepartida@demo.oppytalent.com',
                'Antonia Valenzuela Rojas', 'Chef de partida (entremetier)', 'Chef de Partida (Entremetier) con 6 años de experiencia en hoteles vacacionales de alto volumen. Experta en la elaboración de fondos, salsas y una amplia variedad de platos vegetarianos para bufés de hasta 800 comensales. Destaca por su habilidad en showcooking, obteniendo una valoración de 4.7/5 en encuestas de satisfacción, y por su impacto en la optimización de costes, logrando un ahorro anual de 18.000 € en materias primas.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/da0972b910b641c18dd2c58de41b8c3d_Claudia-Avatar.webp', '+56 9 555 55 555', 'https://www.linkedin.com/in/demo08',
                NULL, NULL, 'Copiapó, Chile',
                '[]', '[]',
                '["Showcooking", "Gesti\u00f3n de stock", "Cocina mediterr\u00e1nea", "Cocina vegetariana", "Control de APPCC", "Trabajo bajo presi\u00f3n", "Creatividad culinaria", "Trabajo en equipo", "Negociaci\u00f3n con proveedores", "Optimizaci\u00f3n de costes"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('b071152b-d0f7-4169-b9c5-e4779f67d7df', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'Hotel Explora Santiago', 'Chef de partida',
                    '2023-03-01', '2025-07-01', '- Elaboración de fondos y platos vegetarianos para el bufé principal.
- Formación de 3 ayudantes de cocina en protocolos de APPCC.
- Negociación con proveedores de productos de Km 0, logrando una reducción de costes del 12%.
- Gestión y control de la partida de entremetier, asegurando la calidad y el cumplimiento de los estándares.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('9c945729-eb60-48fe-9d09-0f06b012e573', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'Hotel Costanera Palace', 'Segunda de cocina',
                    '2019-06-01', '2023-02-01', '- Apoyo directo al Jefe de Cocina en la supervisión y organización de las distintas partidas.
- Elaboración y control de la producción diaria de preparaciones frías y calientes.
- Gestión de inventarios y control de stock para optimizar el uso de materias primas.
- Participación activa en el diseño y mejora de menús, adaptándose a las necesidades de los comensales y eventos.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('4c6da037-ffbc-4dfb-a80c-483ef5fdcdd2', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'Instituto Culinario Austral', 'CFGS Dirección de Cocina',
                    2019, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('750e3a3d-b729-4c1e-8f50-79628316c8f4', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'Instituto Culinario Austral', 'CFGM Técnico en Cocina y Gastronomía',
                    2017, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('885a36e5-b5a7-4b1b-bdf8-2e59e97dfe7b', 'd88b7322-f270-4105-9a35-0c318e2bab73', 'Asociación Chilena de Sommeliers', 'Sommelier Nivel 1',
                    2021, 'Estudio extraído', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-recepcionista';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('7284fcc3-2dd9-4536-903e-4227adc76db7', 'demo-recepcionista', 'recepcionista@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Valentina Paz', 'Aguilar');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('2c51501a-4b17-4b20-bc37-a8854b16d6dc', '7284fcc3-2dd9-4536-903e-4227adc76db7', 'recepcionista@demo.oppytalent.com',
                'Valentina Paz Aguilar Soto', 'Recepcionista - Atención al Cliente', 'Activa, responsable y con muy buena predisposición para el trato con las personas. Me interesa desarrollarme en el área de atención al público, aprendiendo y brindando una experiencia cordial y eficiente. Aspiro a mejorar cada vez un poco mas para crecer tanto en nivel profesional como personal. Tengo facilidad para comunicarse, trabajar en equipo y adaptarme a distintos entornos de trabajo.',
                'https://anonymized-avatars.dev/valentina-aguilar-profile.webp', '+56 9 888 55 333', 'https://www.linkedin.com/in/demo09',
                NULL, NULL, 'Antofagasta, Chile',
                '[]', '[]',
                '["Responsabilidad", "Liderazgo y seguimiento", "Trabajo en equipo", "T\u00e9cnicas de comunicacion afectiva", "Resoluci\u00f3n de problemas", "Capacidad de adaptaci\u00f3n", "Habilidades multitarea"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('eb28d60c-aa57-4c59-990e-d73cae094498', '7284fcc3-2dd9-4536-903e-4227adc76db7', 'Minimarket La Esquina Fresca', 'Atención al público y administración básica',
                    '2024-01-01', '2025-12-31', '- Atención personalizada a clientes, garantizando un trato cordial y eficiente.
- Manejo y cierre de caja diario, control de ingresos y egresos.
- Registro y control de cuentas diarias del negocio.
- Reposición de mercadería y control de stock.
- Mantenimiento del orden, limpieza e higiene del local.
- Organización general del espacio del trabajo para un correcto funcionamiento del negocio.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('4ac464bb-ca6a-411d-bd8d-fe0d5fe8baf4', '7284fcc3-2dd9-4536-903e-4227adc76db7', 'Cafetería ''El Encuentro'' (Mercado Artesanal)', 'Atención al cliente',
                    '2026-06-24', '2023-12-31', '- Atención al cliente como barista y mesera
- Registro y control de cuentas
- Organización general del espacio',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('c26acb0c-8f68-4119-af89-8f84d5a03ac1', '7284fcc3-2dd9-4536-903e-4227adc76db7', 'Liceo Polivalente Gabriela Mistral', 'Secundario Completo',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('882a7c7d-e4b7-4a2b-abcb-b420dabc643c', '7284fcc3-2dd9-4536-903e-4227adc76db7', 'Centro de Formación Técnica Los Andes', 'Licenciatura en economía y administración de empresas',
                    2025, 'Estudio extraído', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-psicologa';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'demo-psicologa', 'psicologa@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Fernanda', 'Contreras');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('2a7e8528-a9db-46d1-bd4a-fc89cfd42305', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'psicologa@demo.oppytalent.com',
                'FERNANDA CONTRERAS', 'PSICÓLOGA LABORAL - CLÍNICA', 'Psicóloga senior con más de 10 años de experiencia en reclutamiento y selección end-to-end en empresas de alta dotación. Especialista en atracción de talento, hunting y entrevistas por competencias, con foco en indicadores, mejora continua e inclusión laboral certificada. He liderado iniciativas de marca empleadora y cultura organizacional, además de diseñar y ejecutar capacitaciones para líderes en liderazgo, feedback, experiencia de cliente, bienestar y ética laboral. Cuento con experiencia en optimización de procesos de RRHH, mapeo de talento y análisis de indicadores para la toma de decisiones. Asimismo, brindé apoyo clínico a más de 2.500 colaboradores, entregando acompañamiento psicológico como parte de un servicio organizacional integral. También colaboré con el área legal en investigaciones internas y gestión de casos laborales.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/8fd13c872513449fa8d4d989dba1f791_Nicole-Avatar.webp', '+56 9 555 55 555', 'https://www.linkedin.com/in/demo10',
                NULL, NULL, 'Talca, Chile',
                '[]', '[]',
                '["Reclutamiento y Selecci\u00f3n", "Atracci\u00f3n de Talento", "Hunting", "Entrevistas por Competencias", "Indicadores", "Mejora Continua", "Inclusi\u00f3n Laboral", "Marca Empleadora", "Cultura Organizacional", "Liderazgo", "Feedback", "Experiencia de Cliente", "Bienestar", "\u00c9tica Laboral", "Optimizaci\u00f3n de Procesos RRHH", "Mapeo de Talento", "An\u00e1lisis de Indicadores", "Apoyo Cl\u00ednico", "Acompa\u00f1amiento Psicol\u00f3gico", "Investigaciones Internas", "Gesti\u00f3n de Casos Laborales", "Excel", "SPSS", "Power BI", "Talana", "SAP Successfactor", "Geovictoria", "Navex", "Visio"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('ea4ac392-d708-4c73-8f73-f0df7ac76a90', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA CUMBRES RH', 'Senior Talent Acquisition & Culture Specialist',
                    '2025-01-01', NULL, '- Lideré procesos de reclutamiento estratégico, fortaleciendo la atracción de talento y la marca empleadora.
- Impulsé iniciativas de cultura organizacional y acompañé a líderes en la gestión y desarrollo de personas, participando en proyectos estratégicos de Recursos Humanos.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('bb8c1344-10ab-40fa-adeb-66290269aaa7', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CORPORACIÓN RETAIL PATAGONIA', 'Generalista de Recursos Humanos',
                    '2022-01-01', '2025-12-31', '- Responsable de la implementación de procesos y políticas de gestión de personas, con foco en eficiencia operativa, cumplimiento normativo y cultura organizacional.
- Atracción y desarrollo de talento, promoviendo un buen clima laboral e impulsando la equidad de género mediante estrategias para aumentar la participación femenina.
- Experiencia en administración de personal, normativas laborales y optimización de dotaciones.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('b64398e6-2123-4db4-940d-8390c63be89a', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CORPORACIÓN RETAIL PATAGONIA', 'Encargada de Reclutamiento y Selección',
                    '2026-06-24', NULL, '- Encargada de selección interna y estratégica, incluyendo levantamiento de perfiles y descriptores de cargo.
- Gestión de R&S: publicación de avisos, filtro curricular, head hunting, entrevistas y elaboración de informes psicolaborales.
- Administración de correos en TI Service Now, enrolamiento en Talana y control de pagos a proveedores.
- Implementación de políticas de inclusión laboral, mapeo de talento y seguimiento de desempeño.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('9105b741-23a3-496c-aa5c-466c12a233fe', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA PRISMA TALENTO SpA', 'Jefa de Reclutamiento y Selección',
                    '2020-01-01', '2022-12-31', '- Responsable de procesos de selección para clientes internos y externos, supervisión de 7 psicólogos y desarrollo de políticas del área.
- Coordinación con departamentos para aplicar buenas prácticas laborales, elaboración de informes para organismos externos y generación de informes KPI.
- También gestionaba la evaluación de satisfacción de clientes para mejorar los procesos de selección.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('974ed0b9-35ca-4bb7-87d7-2e2a6e47c598', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA PRISMA TALENTO SpA', 'Psicóloga Consultora de Reclutamiento y Selección',
                    '2018-01-01', '2020-12-31', '- Responsable de los procesos completos de selección interna y para clientes asignados.
- Experiencia en entrevistas masivas e individuales, aplicación de pruebas y elaboración de informes psicolaborales.
- Gestión de contacto con clientes internos y externos, otros.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('256ca8aa-884d-49ee-9bfb-42cfe0ee9cb6', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'SOLUCIONES MINERAS RRHH', 'Psicóloga Consultora de Reclutamiento y Selección',
                    '2018-01-01', NULL, '- Liderar procesos completos de R&S: Experiencia en entrevistas grupal e individual; Aplicación e interpretación de test (PBLL, grafológico, Lüscher, Disc, Zulliger, etc.); Realización de informes psicolaborales, otros.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('8840510a-2999-42fc-9473-f50e7ca99462', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'MUNICIPALIDAD DE PUEBLO NUEVO', 'Coordinador y facilitador de talleres',
                    '2016-01-01', '2017-12-31', '- Planificación, diseño y ejecución de talleres psicoeducativos en contexto municipal, en articulación con programas sociales y organizaciones como TECHO y Municipalidad de San Bernardo Oriente.
- Responsable de la elaboración de material didáctico y de difusión, gestión de convocatorias territoriales y coordinación logística de actividades.
- Facilitación de grupos en temáticas de crianza positiva, manejo de pataletas, autoestima, empoderamiento femenino, prevención de violencia y apresto laboral, con foco en población en contexto de vulnerabilidad, especialmente mujeres.
- Experiencia en gestión de grupos, acompañamiento psicosocial, evaluación de participantes y seguimiento de procesos, contribuyendo al fortalecimiento de habilidades personales y la inserción social y laboral.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('66c5b922-972c-4980-a1e9-f391c33072be', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'UNIVERSIDAD METROPOLITANA ANDINA', 'Diplomado de técnicas de evaluación psicológicas para selección de personas',
                    2016, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('e00e2454-015b-44de-b92a-171723589982', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'UNIVERSIDAD METROPOLITANA ANDINA', 'Licenciada en psicología',
                    2016, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('8661a6ab-9ed9-4e0e-9894-eb1ab5cdf43b', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'INSTITUTO NACIONAL DE INCLUSIÓN PROFESIONAL', 'Certificación de Gestor de Inclusión Laboral',
                    2023, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('6fcd7fb9-7aca-4ed6-b3c7-3af4f30696e0', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'UMA', 'Diplomado Técnicas de evaluación psicológicas',
                    2016, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('591c463c-f4b3-4cc9-a07d-035317107ce6', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'ACADEMIA CHILENA DE FORMACIÓN EJECUTIVA', 'Curso de Técnicas de análisis de puestos y elaboración de descriptores de cargos',
                    2018, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('b89c2028-baff-4e0b-9621-e9a4ef546327', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CENTRO DE CAPACITACIÓN AVANZADA (CCA)', 'Curso de técnica de evaluación Test Zulliger',
                    2019, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('734f1fe5-e721-41b3-99b2-b1f0359aacde', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'DESARROLLO PROFESIONAL CHILE SpA', 'Curso de técnica de trabajo en equipo y Liderazgo',
                    2019, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('6ecf5146-6820-4be0-a303-b33e8e5b3fde', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA TECNO AVANZADA', 'Curso de Excel intermedio',
                    2021, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('8838c275-c9e1-4d58-9118-96da9ac333f3', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CENTRO DE CAPACITACIÓN AVANZADA (CCA)', 'Herramientas para la evaluación psicolaboral actuales',
                    2024, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('4a4e5127-cb40-47ea-89a5-5971857198f5', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CENTRO DE CAPACITACIÓN AVANZADA (CCA)', 'Curso de power BI básico - intermedio',
                    2024, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('6e724f1b-31af-4788-89d1-50f9952e7c45', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'INSTITUTO DE CAPACITACIÓN LABORAL CHILE', 'Curso de leyes laborales actualizadas',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('76891d9e-4221-4798-9cb6-5571f6757f26', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA ESTRATEGIA CHILE SpA', 'Tácticas de comunicación efectiva',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('9b1556d3-bb59-4660-994f-0da78128e5e4', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'CONSULTORA ESTRATEGIA CHILE SpA', 'Curso actualización ley 21.015 Inclusión y estadística del 1%',
                    2025, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('835ba8fd-dabf-46ff-bcf8-ed27eccb9b6c', 'f2581dcd-a507-4dc9-a279-6f8e31a5ffad', 'ACADEMIA TALENTO Y BIENESTAR', 'Curso Felicidad en el trabajo',
                    2025, 'Estudio extraído', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-tecnicoquimico';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('d87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'demo-tecnicoquimico', 'tecnicoquimico@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Matías', 'Cornejo');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('4131a144-eb97-43e1-854c-eed362e4a9fe', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'tecnicoquimico@demo.oppytalent.com',
                'Matías Cornejo Rojas', 'Técnico Químico | Operario de Producción Industrial | Analista de Control de Calidad', 'Profesional técnico con más de 20 años de trayectoria integral en el sector químico e industrial, abarcando desde la operación pesada en plantas de producción continua y por lotes (batch), hasta el análisis instrumental de alta precisión en laboratorios de Control de Calidad. Destaca por su capacidad para liderar equipos operativos, optimizar tiempos de producción (como la concepción de una envasadora semiautomática) y redactar procedimientos críticos que garantizan el éxito en auditorías. Líder colaborativo orientado al consenso, con fuerte enfoque en la seguridad, la adaptabilidad ante cambios de objetivos y la toma de decisiones basada en la fiabilidad de los procesos.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/placeholder_avatar_industrial.webp', '+56 9 555 55 555', 'https://www.linkedin.com/in/demo11',
                NULL, NULL, 'Rancagua, Chile',
                '[]', '[]',
                '["Operaci\u00f3n Industrial", "An\u00e1lisis de Calidad", "Gesti\u00f3n y Liderazgo", "Sistemas y Herramientas", "SAP", "AS400", "ChemStations", "MS Office", "HPLC", "GC", "Data Color", "Volumetr\u00eda", "Viscosimetr\u00eda", "Control de especificaciones cr\u00edticas", "Liderazgo de turnos", "Control de inventarios", "Redacci\u00f3n de SOPs", "Resoluci\u00f3n de conflictos", "Gesti\u00f3n de emergencias", "Manejo de hornos de fundici\u00f3n", "Ba\u00f1os de esta\u00f1o", "Reactores de s\u00edntesis qu\u00edmica", "Molinos", "Bombas", "Cromatograf\u00eda", "Espectrofotometr\u00eda", "Seguridad", "Adaptabilidad", "Toma de decisiones"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('dff9a953-e837-4728-ae3e-438f609c91a4', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Cristales del Pacífico S.A.', 'Operario de Producción',
                    '2021-01-01', NULL, '- Operación integral del horno de fundición de vidrio, baño de estaño (formación de espesor y ancho) y extendería (recocido y enfriamiento).
- Control estricto de la curva de temperatura en función de la carga operativa del momento, garantizando el cumplimiento de los settings establecidos para la calidad del producto.
- Manejo de planta de mezcla y supervisión de descarga de camiones tolva.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5cab2271-da79-4817-a248-fb8d18ec7d4c', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Reactivos del Maule Ltda. / Colorantes del Valle S.A.', 'Operario de Producción (Encargado) y Analista de Turno',
                    '2008-01-01', '2021-12-31', '- **Gestión de Equipo:** Liderazgo de un turno de 3 personas, evaluando indicadores de productividad y resolviendo conflictos operativos en línea en base a las prioridades de entrega.
- **Logro Destacado:** Ideó e impulsó el desarrollo de una envasadora de baldes semiautomática, lo que redujo drásticamente los tiempos de ciclo y disminuyó el personal necesario en el sector de 2 operarios a 1.
- **Optimización de Procesos:** Confección y actualización de manuales de procedimientos de planta y laboratorio, logrando mejorar tiempos, reducir errores operativos y asegurar la aprobación de auditorias.
- **Producción y Calidad:** Fabricación de pinturas solventes y acuosas mediante el manejo de molinos y dispersoras. Descarga de camiones cisterna con resinas.
- **Ajuste Analítico:** Muestreo y análisis con espectrofotómetro y sistema Data Color. En caso de desvíos, ejecutaba ajustes precisos de matización o dilución (agua/solvente) asegurando correcta pesada y homogeneización.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('462e6876-04f9-48f4-93ce-39fec25fa8ae', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Polímeros Avanzados Chile S.A.', 'Analista de Control de Calidad',
                    '2005-01-01', '2008-12-31', '- Ejecución de determinaciones analíticas críticas para la liberación de lotes, con especial foco en los análisis de cortes de reacción, garantizando tiempos exactos para evitar mermas o degradación del producto.
- Análisis instrumental avanzado: Determinación de concentración por cromatografía gaseosa (HP 5890 II / HP 6890) y líquida (HP 1100 / HP 1200), y absorbancia por espectrofotometría láser.
- Operación de equipos: Diagnóstico de fallas en cromatógrafos, selección y cambio de columnas, y detección de canales obstruidos mediante ChemStation.
- Análisis fisicoquímicos exhaustivos: DQO, punto de fusión, humedad (Karl Fischer / infrarrojo), insolubles, índice de iodo/acidez, viscosidad (Brookfield / Copa Ford) y densidad.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('9f1a1270-dcd3-4ae4-b996-6f07c7773764', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Refinería del Maipo (Grupo AgroInnovación)', 'Operario de Producción',
                    '2003-01-01', '2005-12-31', '- Producción de fertilizantes líquidos y sólidos mediante procesos continuos y batch.
- Manejo de equipos de alta presión/presión negativa y diversidad de bombas bajo estrictos protocolos de seguridad química y lectura obligatoria de procedimientos previos.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5ed6850e-b2e8-445a-9e68-7c431bb7a6c7', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'BioSoluciones Agrícolas S.A.', 'Operario de Producción',
                    '2002-01-01', '2003-12-31', '- Manejo de reactores en planta de síntesis química para la producción de agroquímicos complejos (glifosato, cipermetrina, imazetapir).',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('7b4c9774-db29-417b-acf9-d6346c63b8a9', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Centro de Formación Técnica ''Austral Químico''', 'Técnico Químico',
                    2001, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('2411634f-9d95-48fb-980e-3185dfa15b0c', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Academia Analítica del Sur', 'Cromatografía Líquida HPLC',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('e9b77550-515a-41f5-8644-9fe4804b5673', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Academia Analítica del Sur', 'Operador y Mantenimiento / Diagnóstico de fallas de HPLC 1100 y 1200',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('fc07ede2-ea0a-40d7-aa5d-6ace2084cb19', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Academia Analítica del Sur', 'Cromatografía Gaseosa HP6890 / HP5890 y operación con ChemStations',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('81a8f852-bc88-4d9e-98bd-7b42b913774f', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Licencia de Conducir', 'A 1.4',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('4310b66c-01f9-4671-a3f7-107945e0674b', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Licencia de Conducir', 'B 1',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('383038f4-0bac-44ad-8936-337e2249abef', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Disponibilidad', 'Disponibilidad Full-time',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('fd2d8893-0382-4b71-8d67-48d1614f9ce4', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Disponibilidad', 'Disponibilidad Part-time',
                    'Detalle de la habilitación', NULL, true);
INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('fb71020d-40c5-4241-a75a-fdaeadee5dbe', 'd87c0e48-43c2-4b4b-8d4f-34a1f861da26', 'Disponibilidad', 'Disponibilidad Turnos rotativos',
                    'Detalle de la habilitación', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-abogado';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('f659d3a2-d48a-438e-845c-5916869ec034', 'demo-abogado', 'abogado@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Valeria', 'Rojas');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('f75eedd5-89d5-4817-89a7-656396bc812c', 'f659d3a2-d48a-438e-845c-5916869ec034', 'abogado@demo.oppytalent.com',
                'VALERIA ANTONIA ROJAS SOTO', 'LIC. EN DERECHO', 'Me considero una persona responsable, proactiva, creativa, y con facilidad para aprender rápido, me apasiona trabajar en equipo, desarrollar soluciones eficientes, alcanzar objetivos, mi enfoque profesional se enfoca en la resolución de problemas y las innovaciones.',
                'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/72ba2b4895714c4ea58f8368518538bb_Vania-Avatar.webp', '+56 9 888 55 333', 'https://www.linkedin.com/in/demo12',
                NULL, NULL, 'La Serena, Chile',
                '[]', '[]',
                '["Liderazgo", "Comunicaci\u00f3n asertiva", "Gesti\u00f3n de activos", "Resoluci\u00f3n de problemas", "Elaboraci\u00f3n de reportes", "Trabajo en equipo", "Word", "Excel", "PowerPoint", "Zoom", "Google Meet"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5ebb6289-bf3f-4d6a-b143-c47ca45d0f95', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Fiscalía Regional Metropolitana Oriente, División de Delitos Complejos', 'Pasante en el Área Administrativa',
                    '2023-10-01', '2024-04-01', '- Redacción de órdenes de aprehensión
- Inicio de carpetas de investigación
- Realización de confrontas
- Entrevistas a usuarios
- Solicitud de promociones dentro de juzgados
- Trabajo bajo presión',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('d14d655a-fc2a-4c1a-bc7e-40b0ff64db49', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Estudio Jurídico Veritas & Partners', 'Pasante',
                    '2024-05-01', '2025-02-01', '- Elaboración de contratos
- Gestión y seguimiento de asuntos legales
- Atención a clientes y proveedores',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('ddab5d19-30c9-4971-ae28-19caba81d503', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Logística Andes Express', 'Monitorista',
                    '2025-03-01', '2025-06-01', '- Manejo de monitoreo de distintas unidades mediante GPS
- Atención al cliente para información sobre paquetes',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('93df87a9-a40c-437f-8f68-933e2488af7b', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Bufete Jurídico Cruchaga & Ossa', 'Pasante',
                    '2025-06-01', '2025-09-01', '- Atención de asuntos legales en materia penal, civil y laboral
- Redacción de escritos',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('93213786-42f2-415d-bccf-f4a97136dc66', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Universidad Metropolitana de Leyes', 'Licenciatura en Derecho',
                    2026, 'Estudio extraído', NULL, true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('d74f3f4b-2c24-4611-8f82-cbd579941e38', 'f659d3a2-d48a-438e-845c-5916869ec034', 'Universidad Metropolitana de Leyes', 'Diplomado en proceso penal acusatorio',
                    2026, 'Estudio extraído', NULL, true);
DELETE FROM oppy.usuarios WHERE username = 'demo-profesordequimica';
INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('ce2979fe-b849-4153-be41-8e042002d2d9', 'demo-profesordequimica', 'profesordequimica@demo.oppytalent.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, 'Elena', 'Rojas Morales');
INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('ed69c9d8-37d6-4d24-88ab-8a86a3eb0178', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'profesordequimica@demo.oppytalent.com',
                'ELENA ROJAS MORALES', 'Profesor de Química de Secundaria', 'Apasionada por la enseñanza con más de 5 años de experiencia en química. Excelentes habilidades en la enseñanza y manejo de laboratorios. Contribuyó a un aumento del 15% en los puntajes del examen de química AP.',
                NULL, '+56 9 888 55 333', 'https://www.linkedin.com/in/demo13',
                NULL, NULL, 'La Serena, Chile',
                '[]', '[]',
                '["Qu\u00edmica", "Manejo de Laboratorios", "Ense\u00f1anza de IB", "Preparaci\u00f3n para AP", "Gesti\u00f3n de Proyectos", "Tecnolog\u00edas Educativas", "Innovador", "Enfocado en Resultados"]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('6ab2ca7a-6f5a-42e0-ba07-46e8ff9aff65', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Liceo Bicentenario Cordillera Andina', 'Profesor de Química',
                    '2020-09-01', NULL, '- Desarrollé y llevé a cabo un currículo de química que alineó con los estándares de IB, logrando un aumento del 17% en la comprensión conceptual de los estudiantes.
- Implementé un nuevo sistema de gestión de laboratorio que mejoró la eficiencia en un 25% y redujo los costos de desperdicio de reactivos.
- Organicé cinco ferias de ciencias, incluyendo un evento regional que atrajo a más de 500 participantes.
- Enseñé cursos avanzados de química, logrando que el 85% de los estudiantes obtuvieran calificaciones superiores a 4 en sus exámenes IB.
- Lideré un proyecto de investigación sobre el uso de tecnologías emergentes en la enseñanza de la química, presentando resultados en una conferencia nacional.
- Creé un programa de tutorías después de clases, lo que resultó en una mejora del 20% en los resultados del examen final de los estudiantes.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('2b82313c-838f-44ff-a631-5ada0962e3b8', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Instituto Profesional del Biobío', 'Profesor de Química',
                    '2016-08-01', '2020-08-01', '- Desarrollé un plan de estudios de química avanzada para preparar a los estudiantes para exámenes AP, incrementando las notas promedio en un 15%.
- Coordiné y llevé a cabo entrenamientos de seguridad en laboratorios para más de 200 estudiantes anuales, garantizando cero accidentes durante los últimos tres años.
- Diseñé y ejecuté experimentos de laboratorio innovadores que mejoraron la comprensión práctica y teórica de los estudiantes en un 20%.
- Lideré cursos extracurriculares de preparación para competencias de química, logrando que tres equipos calificaran para la etapa nacional.
- Mantuve una tasa de asistencia estudiantil del 98%, destacando por crear un ambiente de aprendizaje atractivo y estimulante.',
                    '[]', true);
INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('5016ab59-ab17-4c94-af84-0e13ef9ab460', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Universidad Metropolitana de Ciencias y Humanidades', 'Asistente de Laboratorio de Química',
                    '2014-01-01', '2016-07-01', '- Apoyé en la preparación y ejecución de protocolos de laboratorio para cursos de química general y orgánica.
- Supervisé a un equipo de 10 asistentes de laboratorio, asegurando el cumplimiento de las normas de seguridad y la precisión en la preparación de reactivos.
- Colaboré en un proyecto de investigación que resultó en la publicación de un artículo en una revista indexada.
- Creé materiales didácticos que mejoraron la comprensión de conceptos complejos en un 30% según las evaluaciones estudiantiles.',
                    '[]', true);
INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('b39369ec-81d7-4bcb-84f8-b001c502b53c', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Universidad Austral del Maipo', 'Maestría en Educación',
                    2018, 'Estudio extraído', NULL, true);
INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('46b427bb-aa77-410b-8901-0e5023de5246', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Proyecto de investigación sobre el uso de tecnologías emergentes en la enseñanza de la química', 'Lideré un proyecto de investigación sobre el uso de tecnologías emergentes en la enseñanza de la química, presentando resultados en una conferencia nacional.',
                    'Lideré un proyecto de investigación sobre el uso de tecnologías emergentes en la enseñanza de la química, presentando resultados en una conferencia nacional.', '["Tecnolog\u00edas Educativas", "Investigaci\u00f3n", "Qu\u00edmica"]',
                    'null', '["Tecnolog\u00edas Educativas", "Investigaci\u00f3n", "Qu\u00edmica"]',
                    NULL, NULL, NULL, CURRENT_DATE, true);
INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('1a54b595-41e7-45a4-a87c-0eb2c3719209', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Logro', 'Incremento en Puntajes de AP Química',
                    'AP Química', NULL, 'Mejoré los puntajes de AP Química en un 15% en dos años mediante técnicas de instrucción innovadoras y tutorías personalizadas.', NULL, true);
INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('7134d9e8-4e7d-47bb-a74f-d36b16bef16e', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Logro', 'Desarrollo de Programa IB de Química',
                    'IB Química', NULL, 'Implementé y gestioné un nuevo programa de Química IB, aumentando la participación estudiantil en un 20%.', NULL, true);
INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('dac990fb-19fc-4c83-8798-5ce00b0d59bc', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Logro', 'Laboratorio Escolar Eficiente',
                    'Lab', NULL, 'Reduje el tiempo de preparación de reactivos de laboratorio en un 30% mediante una mejor organización y gestión de recursos.', NULL, true);
INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('599f1836-e9ab-431a-8d09-fd4162cc71ca', 'ce2979fe-b849-4153-be41-8e042002d2d9', 'Logro', 'Capacitación en Evaluación de Laboratorio',
                    'Lab', NULL, 'Capacité a 50 docentes en evaluaciones prácticas de laboratorio, mejorando la infraestructura educativa y la calidad de la enseñanza.', NULL, true);
DELETE FROM oppy.usuarios WHERE email = 'jcampillayworks@gmail.com';

INSERT INTO oppy.usuarios 
    (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
    is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
    VALUES ('00000000-0000-4000-8000-000000000000', 'jcampillay', 'jcampillayworks@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA', 'ADMIN', true, false, true, false, true, true, 1000, 0, 0, '[]'::json, 'Jaime', 'Campillay');


INSERT INTO oppy.perfiles 
    (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
    telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
    VALUES ('e99d5dd7-c9af-4aba-b419-0837048cdcb5', '00000000-0000-4000-8000-000000000000', 'jcampillayworks@gmail.com',
    'Jaime Gabriel Campillay Rojas', 'INGENIERO CIVIL INDUSTRIAL | SENIOR SOFTWARE & DATA ENGINEER', '¡Hola! Soy **Jaime Campillay**, un profesional apasionado por el punto de encuentro entre la **Ingeniería, los Datos y la Tecnología con propósito**. Mi viaje profesional está impulsado por una curiosidad inagotable, la auto-superación constante y la convicción de que la mejor tecnología es aquella que resuelve problemas reales, mejora la experiencia humana y abre nuevas oportunidades en armonía con nuestro entorno.

---

### 💼 Mi Trayectoria: El Puente entre Estrategia y Ejecución

Poseo una formación como **Ingeniero Civil Industrial** y un **Magíster en Ingeniería Industrial y de Sistemas**. A diferencia del desarrollo de software tradicional, mi enfoque nativo proviene del pensamiento sistémico, la optimización de procesos y la visión de negocios. Sin embargo, mi profundo amor por la programación me llevó a convertirme en **Lead Full-Stack Software Engineer** y **Especialista en Ingeniería de Datos**.

A lo largo de mi carrera, he tenido el privilegio de diseñar e implementar soluciones de alta complejidad en sectores sumamente exigentes:
* **Gran Industria y Minería:** Optimizando la reportabilidad y el control operacional en terreno bajo condiciones extremas (Mina Los Bronces).
* **Banca y Finanzas Corporativas:** Diseñando robustos robots transaccionales (RPA en UiPath REFramework), pipelines ETL de migración cloud (GCP/Talend) e integraciones analíticas complejas para la mitigación de riesgos cambiarios en mesas de dinero.
* **Consultoría Tecnológica de Vanguardia:** Modelando hojas de ruta de infraestructura crítica y arquitecturas híbridas (Docker y Kubernetes) para el procesamiento interbancario del país.

---

### 🚀 Emprendimiento e Innovación Humana

Hoy en día, canalizo toda esta experiencia acumulada como **Fundador de OppyChat**, una plataforma EdTech impulsada por Inteligencia Artificial y arquitecturas asíncronas en tiempo real. Este proyecto nació de mi propio camino y aspiración por dominar el idioma inglés, y representa fielmente mi visión de la tecnología: utilizar modelos avanzados de IA no como herramientas frías, sino como puentes interactivos y personalizados para ayudar a las personas a romper barreras comunicativas y conectar con una audiencia global.

---

### 🌿 Filosofía de Vida: Equilibrio, Lógica y Gratitud

Más allá de las líneas de código, las bases de datos y la nube, creo firmemente en un enfoque de vida equilibrado e íntegro. Encuentro mi balance ideal combinando la rigurosidad analítica con la expresión creativa a través de la **música y la guitarra**, una práctica que me permite entrelazar la lógica y la intuición de una forma profundamente satisfactoria.

Mi conexión con la Tierra es profunda y espiritual. Considero que cada rincón de nuestra naturaleza y cada ser vivo albergan un valor incalculable que merece nuestro respeto, cuidado y gratitud. Para mí, el **trekking y el senderismo** en la alta montaña no son solo pasatiempos para mantenerme físicamente activo; son espacios sagrados de desconexión y reflexión que me inspiran, me devuelven la perspectiva y me recuerdan nuestro deber colectivo de proteger y preservar la belleza y diversidad de la Tierra para las generaciones futuras.

Afronto cada proyecto, cada célula de trabajo en equipo y cada línea de código con alegría, resiliencia y el compromiso de generar un impacto que sea técnicamente excelente, económicamente viable y ambientalmente consciente. 

*¿Construimos algo significativo juntos?*',
    'https://pub-693986afee154b369b5ca2b96d341053.r2.dev/a49b10ecb3cc4b3e857f183c5b3e29c4_Foto_Personal.webp', '+569-81394911', 'https://www.linkedin.com/in/jaime-campillay/',
    'https://github.com/jcampillay8', NULL, 'SANTIAGO, CHILE',
    '[]'::json, '[]'::json, '["Modelos de Lenguaje Grandes (LLM", "GenAI)", "Python (Polars", "Pandas", "Flask", "FastAPI)", "SQL Avanzado", "PostgreSQL", "MySQL", "SQL Server", "Pipelines de Datos (ETL)", "Google Cloud Platform (GCP)", "Microsoft Azure Data", "Docker", "Control de Versiones (Git)", "Linux", "Dashboards de Visualizaci\u00f3n (Dash", "Plotly", "Power BI", "D3.js)", "An\u00e1lisis de Confiabilidad de Activos (MTBF", "MTTR)", "Control de Gesti\u00f3n Operativa", "Metodolog\u00edas \u00c1giles"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('85b24b66-3dbf-4694-ade1-e2e004d7f84a', '00000000-0000-4000-8000-000000000000', 'TECHINT - Ingeniería & Construcción', 'Ingeniero Analista en Programación y Control de Gestión',
    '2019-04-01', '2020-10-01', '## Analista Programador y Control de Gestión — Techint  
**Proyecto Mina Los Bronces | Servicios para Anglo American**  
*2019 – 2020*

- **Analítica de Avance y Reportabilidad (HH Ganadas vs. Gastadas):** Responsable del monitoreo y análisis de avances físicos para el proyecto de reemplazo de tuberías en Mina Los Bronces. Desarrollé reportes ejecutivos y métricas comparativas entre avance real y planificación (*schedule*), con especial foco en el control y balance de **Horas Hombre (HH) ganadas versus HH gastadas**, facilitando la toma de decisiones basada en datos para la gerencia de obra.

- **Liderazgo y Coordinación de Equipos Operacionales:** Supervisé y coordiné un equipo de entre **9 y 15 apuntadores distribuidos en múltiples frentes de trabajo**, asignando tareas, monitoreando el cumplimiento de actividades diarias y asegurando la correcta captura y entrega de reportes operacionales. Actué como punto central de coordinación entre terreno y oficina, garantizando la calidad, oportunidad y consistencia de la información utilizada para la gestión del proyecto.

- **Digitalización y Automatización de Procesos (Excel y Macros):** Diseñé y desarrollé **ReportWorks**, una aplicación móvil orientada a la captura de datos en terreno. En paralelo, implementé automatizaciones avanzadas en **Excel mediante Macros (VBA)** y **Google Apps Script** para la consolidación de información operacional, reduciendo tareas manuales y optimizando significativamente la generación de reportes diarios consolidados.

- **Gestión de Datos y Automatización de Estados de Pago:** Lideré la consolidación y validación de información asociada al proceso de **Estado de Pago**. Desarrollé herramientas basadas en Excel y macros para automatizar el cruce de datos provenientes de múltiples fuentes, asegurando consistencia, trazabilidad y confiabilidad entre documentación técnica, registros de terreno y antecedentes financieros del proyecto.

- **Estandarización de Operaciones en Terreno:** Trabajé directamente con equipos operativos y personal de terreno (“Apuntadores”) para estructurar y normalizar la captura de datos de obra, mejorando la calidad de la información utilizada en reportabilidad mensual y control de avance contractual.

- **Optimización del Flujo de Información y Control Contractual:** Implementé mejoras en la comunicación entre terreno y oficina mediante tableros de control automatizados y seguimiento digital de desviaciones operacionales, permitiendo una gestión más eficiente de contratos, notas de cambio y control documental.

- **Integración entre Ingeniería y Tecnología:** Combiné conocimientos de control de gestión, análisis operacional y desarrollo de soluciones digitales (**Excel, VBA y Google Apps Script**) para impulsar iniciativas de automatización y analítica de datos en un entorno minero de alta exigencia operacional.', '["Miner\u00eda", "Ingenier\u00eda", "Ingenier\u00eda Civil Industrial", "Control de Gesti\u00f3n", "Transformaci\u00f3n Digital", "Automatizaci\u00f3n", "Anal\u00edtica de Datos", "Data Analytics", "Software Development", "Desarrollo de Software", "Gesti\u00f3n de Proyectos", "Reportabilidad", "Business Intelligence", "Optimizaci\u00f3n de Procesos", "Google Apps Script", "Gesti\u00f3n Operacional", "Digitalizaci\u00f3n", "Control de Avance", "Ingenier\u00eda de Datos", "Operaciones Mineras", "Excel", "Macros"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('631cdc21-6112-46b2-9a5c-c2deb31a7664', '00000000-0000-4000-8000-000000000000', 'EY - Building a Better Working World', 'Desarrollador RPA',
    '2021-08-01', '2022-12-30', '## Desarrollador RPA — EY  
*2021 – 2022*

- **Automatización de Ingestión y Procesamiento de Datos:** Diseñé e implementé flujos automatizados para la extracción, transformación y carga de datos provenientes de múltiples fuentes, incluyendo Bases de Datos, APIs, archivos Excel y documentos PDF. Estas soluciones permitieron optimizar procesos críticos de integración de información y reducir significativamente la intervención manual en tareas operativas.

- **Ingeniería de Datos y Procesos ETL:** Desarrollé soluciones de extracción y limpieza de datos no estructurados asociados a documentación legal y notarial, transformando información compleja en registros normalizados y listos para su integración en plataformas bancarias y sistemas corporativos.

- **Integración de Sistemas y Automatización con APIs:** Implementé integraciones mediante APIs y soluciones desarrolladas en Python para validación de identidad, actualización masiva de registros y sincronización de información en tiempo real, asegurando trazabilidad, consistencia y confiabilidad de los datos procesados.

- **Desarrollo de Lógica de Negocio y Validación de Datos:** Programé reglas avanzadas de validación para el procesamiento automatizado de grandes volúmenes de ventas y transacciones diarias, garantizando el cumplimiento de estándares de calidad de datos y requisitos funcionales definidos por el negocio.

- **Optimización de Procesos con RPA:** Implementé soluciones utilizando UiPath (REFramework) y SQL para automatizar procesos de alta carga operativa, logrando mejoras significativas en tiempos de ejecución, eficiencia operacional y disponibilidad de información para análisis y toma de decisiones.

- **Transformación Digital y Automatización Empresarial:** Participé en iniciativas de automatización orientadas a mejorar la eficiencia organizacional mediante la combinación de RPA, integración de sistemas, analítica de datos y desarrollo de soluciones escalables para entornos corporativos de alta demanda.', '["RPA", "UiPath", "Python", "SQL", "ETL", "Data Engineering", "API Integration", "Process Automation", "Backend Development", "Data Processing", "Digital Transformation", "Business Intelligence", "Workflow Automation", "REST APIs", "Software Engineering", "Data Validation", "Enterprise Automation"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('c681131b-0148-4977-8e9b-59b1973f4805', '00000000-0000-4000-8000-000000000000', 'Inexoos', 'Ingeniero Software Semi-Senior',
    '2024-08-01', '2025-03-01', '## Ingeniero de Software Semi-Senior — Inexoos  
*2024 – 2025*

- **Modelado y Arquitectura de Datos:** Diseñé y normalicé modelos de bases de datos relacionales orientados a la gestión masiva de trámites digitales, asegurando integridad referencial, escalabilidad y optimización de consultas en entornos de alta disponibilidad y procesamiento intensivo de información.

- **Desarrollo de Lógica de Negocio y Validación de Procesos:** Implementé lógica de negocio avanzada para la validación y control de flujos de datos críticos, integrando Firma Electrónica Avanzada (FEA) y servicios de georreferenciación para garantizar trazabilidad, consistencia y confiabilidad de la información procesada.

- **Desarrollo Backend e Integración de Sistemas:** Construí y mantuve APIs RESTful utilizando Flask, actuando como núcleo de integración entre servicios backend y aplicaciones frontend. Automaticé flujos de intercambio de información y optimicé tiempos de respuesta en el procesamiento de documentos y operaciones transaccionales.

- **Desarrollo Frontend y Experiencia de Usuario:** Diseñé interfaces dinámicas e interactivas con Vue.js 3, incorporando filtros avanzados, autocompletado inteligente y herramientas de búsqueda optimizadas para facilitar la exploración y análisis eficiente de grandes volúmenes de registros digitales.

- **Optimización de Seguridad y Disponibilidad:** Resolví desafíos técnicos asociados a autenticación, configuración de políticas de seguridad (CORS) y estabilidad de servicios, asegurando la protección de datos sensibles y la continuidad operacional bajo estándares corporativos.

- **Ingeniería de Software y Transformación Digital:** Participé activamente en el desarrollo de soluciones tecnológicas orientadas a la digitalización de procesos documentales, combinando arquitectura de software, automatización e integración de datos para mejorar la eficiencia operacional y la experiencia de usuario.

- **Colaboración Técnica y Resolución de Problemas:** Trabajé en coordinación con equipos multidisciplinarios para analizar requerimientos funcionales, proponer soluciones escalables y resolver incidencias críticas en entornos de desarrollo y producción.', '["Full Stack Developer", "Backend Engineer", "Flask", "Vue.js", "Vue 3", "Python", "REST APIs", "PostgreSQL", "SQL", "API Development", "Database Design", "Authentication", "CORS", "Software Architecture", "Data Processing", "Web Development", "System Integration", "High Availability Systems", "Scalable Applications"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('0719f154-b872-4ecf-8ff4-e807134d3899', '00000000-0000-4000-8000-000000000000', 'OppyChat SpA', 'Founder & Lead Architect (Ingeniería de IA y Datos)',
    '2025-06-01', '2025-04-01', '## Founder & Lead Full-Stack Software Engineer — OppyChat  
*2025 – Actualidad*

- **Arquitectura de Software y Plataforma Escalable:** Diseñé y lideré el desarrollo de una plataforma EdTech impulsada por Inteligencia Artificial enfocada en aprendizaje inmersivo de inglés mediante Role Play conversacional. Construí una arquitectura moderna basada en Python (FastAPI), PostgreSQL, Redis y WebSockets, permitiendo procesamiento en tiempo real, alta disponibilidad y escalabilidad de servicios.

- **Ingeniería de Datos y Automatización de Flujos:** Implementé pipelines de datos y flujos ETL para la ingestión, procesamiento y almacenamiento de conversaciones generadas por usuarios y modelos de IA. Automaticé el intercambio de información mediante APIs RESTful y comunicación en tiempo real utilizando WebSockets.

- **Desarrollo de Inteligencia Artificial y NLP:** Integré Large Language Models (LLMs) como GPT y Gemini para construir motores conversacionales inteligentes orientados al aprendizaje adaptativo. Desarrollé lógica de procesamiento de lenguaje natural (NLP) para clasificación automática de errores lingüísticos en múltiples categorías, transformando conversaciones no estructuradas en métricas analíticas accionables.

- **Sistemas Inteligentes Basados en Datos:** Diseñé un motor de “Práctica Just-in-Time” impulsado por analítica de comportamiento y detección de patrones de error recurrentes, generando ejercicios personalizados de manera automática para optimizar la retención, comprensión y progreso de los usuarios.

- **Persistencia de Contexto y Gestión de Memoria Conversacional:** Implementé soluciones híbridas de almacenamiento utilizando PostgreSQL y Redis para gestionar estados conversacionales complejos, memoria persistente y recuperación eficiente de contexto, mejorando la continuidad y calidad de interacción de los agentes de IA.

- **Visualización de Datos y Product Analytics:** Construí dashboards y herramientas de monitoreo para análisis de comportamiento de usuarios, métricas de uso y seguimiento de rendimiento del sistema, facilitando la toma de decisiones basada en datos para evolución del producto y experiencia de usuario.

- **Seguridad, Infraestructura y DevOps:** Implementé mecanismos de autenticación y autorización mediante OAuth 2.0 y JWT, asegurando protección de datos y control de acceso seguro. Gestioné despliegues e infraestructura utilizando Docker y flujos CI/CD para automatizar procesos de integración y entrega continua.

- **Liderazgo Técnico y Desarrollo Full-Stack:** Lideré de manera integral el diseño de producto, arquitectura backend, desarrollo frontend, integración de IA y estrategia tecnológica del proyecto, combinando ingeniería de software, analítica de datos y experiencia de usuario en una solución SaaS moderna orientada a educación y productividad.', '["Artificial Intelligence", "EdTech", "Product Engineering", "Data Engineering", "Analytics", "Software Architecture", "Full Stack Development", "Generative AI", "Conversational AI", "FastAPI", "PostgreSQL", "Redis", "Automation", "Digital Transformation", "Product Analytics", "Startup Founder", "SaaS Development", "Intelligent Systems"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('71c49042-9828-4525-98e9-87ed86046a27', '00000000-0000-4000-8000-000000000000', 'EY - Building a Better Working World', 'Ingeniero Datos',
    '2023-01-02', '2024-03-22', '## Ingeniero de Datos — EY  
*2023 – 2024*

- **Ingeniería de Datos y Procesos ETL:** Diseñé, desarrollé y optimicé pipelines de datos para proyectos del sector bancario, incluyendo iniciativas para Banco BICE Inversiones. Automaticé procesos de extracción, transformación y carga (ETL) utilizando SQL, Stored Procedures y Talend, asegurando la integridad, calidad y disponibilidad de grandes volúmenes de información crítica en entornos corporativos de alta exigencia.

- **Migración y Consolidación de Datos Estratégicos:** Participé en procesos complejos de migración y normalización de datos financieros hacia plataformas centralizadas, garantizando consistencia entre múltiples fuentes de información y mejorando la confiabilidad de los datos utilizados en análisis operacionales y regulatorios.

- **Modelado Analítico y Gestión de Riesgos Financieros:** Desarrollé soluciones analíticas orientadas a la mitigación de riesgos cambiarios para Banco Internacional, aplicando técnicas de procesamiento y análisis de datos para transformar variables financieras en información accionable para estrategias de cobertura y toma de decisiones basada en evidencia.

- **Desarrollo de Herramientas de Visualización y Monitoreo:** Construí aplicaciones y dashboards interactivos utilizando Python, Pandas y Dash para el monitoreo de KPIs, métricas de riesgo e indicadores financieros, facilitando el acceso centralizado a información crítica para equipos técnicos y áreas de negocio.

- **Optimización de Data Warehouse y Rendimiento de Consultas:** Colaboré en la integración y consolidación de múltiples fuentes de datos hacia entornos PostgreSQL, optimizando estructuras de almacenamiento, consultas SQL y procesos de acceso a información estratégica para mejorar la eficiencia operativa y analítica.

- **Integración entre Negocio y Tecnología:** Actué como nexo entre equipos de negocio y áreas técnicas, traduciendo requerimientos financieros complejos en soluciones de ingeniería de datos, automatización y análisis, alineadas con objetivos estratégicos y estándares corporativos.

- **Transformación Digital Basada en Datos:** Participé en iniciativas orientadas a fortalecer capacidades analíticas y de inteligencia de negocio mediante automatización, visualización de datos y modernización de procesos de gestión de información financiera.', '["Data Engineering", "Python", "SQL", "PostgreSQL", "ETL Pipelines", "Talend", "Data Warehousing", "Backend Data Processing", "Data Analytics", "Business Intelligence", "Dashboard Development", "Pandas", "Dash", "API Integration", "Data Modeling", "Big Data", "Financial Data", "Data Transformation", "Data Migration", "Analytics Engineering"]'::json, true);


INSERT INTO oppy.experiencias 
    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
    VALUES ('ce67e917-91b3-4cec-aa50-b8aa2d78dbb7', '00000000-0000-4000-8000-000000000000', 'ClearPix', 'Co-Founder & Director de Operaciones y Tecnología',
    '2016-11-01', '2018-01-31', '* **Co-Fundación y Gestión Integral en Equipo:** Co-fundé y lideré junto a mi socio un emprendimiento en Valparaíso dedicado al diseño, confección y personalización de indumentaria textil corporativa y particular. Formamos un equipo multidisciplinario y colaborativo donde apoyé tanto en las labores operativas de producción como en la estrategia comercial, logrando duplicar las ventas entre los periodos de 2015 y 2016.

* **Transformación Digital e Implementación de Odoo ERP:** Diseñé, parametricé e implementé el sistema Odoo ERP como el núcleo tecnológico de la empresa. Centralicé los flujos de ventas, compras y contabilidad en una única plataforma, eliminando el trabajo manual y garantizando un control riguroso sobre las transacciones diarias y los costos del negocio.

* **Optimización de Supply Chain e Inventarios:** Configuré y automaticé las reglas de reabastecimiento y control de existencias dentro del módulo de Inventario de Odoo. Esto permitió realizar un seguimiento en tiempo real del stock de prendas de vestir personalizadas, optimizar la cadena de suministro de materias primas y reducir drásticamente los quiebres de inventario.

* **Pivot de Modelo de Negocio y Resiliencia:** Ante la necesidad de cerrar la tienda física en 2017, lideré la reestructuración operativa para mudar el taller de vuelta al garaje y migrar toda la operación hacia canales de comercio digital (E-commerce). La estrategia fue tan exitosa que la demanda digital llegó a superar nuestra capacidad de producción inicial.

* **Vinculación Institucional e Impacto Social:** Participé en el diseño de una alianza estratégica con la Fundación Universidad de Playa Ancha para presentar nuestro modelo de trabajo. Esto nos permitió adjudicarnos y ejecutar un proyecto de reinserción social del Gobierno de Chile, dictando clases de serigrafía y equipación gráfica en el Centro Penitenciario de Valparaíso.', '["\"Emprendimiento\"", "\"Co-Founder\"", "\"Odoo\"", "\"ERP\"", "\"Implementaci\u00f3n de Sistemas\"", "\"Gesti\u00f3n de Operaciones\"", "\"Optimizaci\u00f3n de Procesos\"", "\"Transformaci\u00f3n Digital\"", "\"E-commerce\"", "\"Gesti\u00f3n de Inventarios\"", "\"Supply Chain\"", "\"Proyectos de Impacto Social\""]'::json, true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('eee38da3-2bec-4471-a29e-8f31f0f268c7', '00000000-0000-4000-8000-000000000000', 'Universidad Andrés Bello', 'Ingeniero Civil Industrial',
    2017, '### Perfil de Egreso

El **Ingeniero(a) Civil Industrial** de la Universidad Andrés Bello es un profesional **autónomo, analítico y flexible**, con un marcado **pensamiento sistémico** y la capacidad de liderar y colaborar en **equipos multidisciplinarios** dentro de un contexto globalizado. Su sello profesional se sustenta en los valores de excelencia, integridad y responsabilidad social, abordando sus desafíos con una visión pluralista y respetuosa.

Posee competencias avanzadas de comunicación efectiva (oral y escrita) y está capacitado para desenvolverse fluidamente en entornos cotidianos, laborales y académicos en el idioma **inglés**.

#### Competencias Clave y Áreas de Dominio:

* **Gestión Estratégica y Operaciones:** Capacidad para gestionar estratégicamente organizaciones, diseñando estrategias y soluciones óptimas tanto en la **producción de bienes** como en la **prestación de servicios**.
* **Inteligencia de Negocios y Transformación Digital:** Especialista en dirigir procesos bajo un enfoque de **Business Intelligence (BI)** y herramientas tecnológicas modernas, respondiendo con agilidad a los desafíos de la **transformación digital** en ámbitos industriales, empresariales e institucionales.
* **Ciencia de Datos (Data Science):** Sólidos conocimientos para aplicar la analítica de datos en la identificación de patrones e información crítica que sirva de apoyo fundamental para la **toma de decisiones** en beneficio de la organización.
* **Ingeniería de Proyectos:** Facultad para administrar proyectos, dirigir grupos de trabajo y analizar el desempeño de sistemas productivos bajo un estricto enfoque de **sostenibilidad**.

---

### Licenciatura en Ciencias de la Ingeniería

Como **Licenciado(a) en Ciencias de la Ingeniería**, el graduado está facultado para:
* Aplicar principios científicos y metodologías de ingeniería en la resolución de problemas complejos.
* **Formular y evaluar proyectos** respaldados por herramientas de decisión técnicas y económicas.
* Presentar **soluciones innovadoras** a problemáticas actuales de las organizaciones y la sociedad.', 'https://facultades.unab.cl/ingenieria/carrera/ingenieria-civil-industrial/#:~:text=El%20Ingeniero%20Civil%20Industrial%20de,entregando%20soluciones%20integrales%20e%20innovadoras.', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('22867b69-0940-4698-bab2-37aa60a986e1', '00000000-0000-4000-8000-000000000000', 'Universidad del Desarrollo', 'Magíster en Ingeniería Industrial y de Sistemas',
    2019, '### Objetivos del Programa

El propósito central del programa es formar profesionales altamente competentes en la **ideación, diseño, evaluación y gestión de soluciones innovadoras y sostenibles** aplicadas a:
* Procesos y operaciones industriales.
* Sistemas organizacionales.
* Tecnologías emergentes.

El magíster está diseñado para potenciar la **toma de decisiones estratégicas basadas en datos** (Data-Driven Decision Making) y la gestión integral de proyectos reales en vinculación con la industria. Todo esto con el fin de transformar las prácticas de gestión en entornos globales, competitivos y dinámicos, aportando un valor significativo tanto al sector productivo como a la sociedad.

---

### Perfil del Graduado

El graduado es un líder con **visión sistémica** y sólidas competencias interpersonales, plenamente capacitado para diseñar, optimizar y gestionar sistemas complejos mediante la innovación tecnológica y el análisis avanzado de datos.

#### Competencias Core:

* **Optimización de Operaciones:** Especialista en mejorar la eficiencia y competitividad empresarial a través de la gestión de la **cadena de suministro (Supply Chain)**, logística avanzada y metodologías de **mejora continua**.
* **Gestión Organizacional Estratégica:** Capacidad para integrar estrategias corporativas clave, abarcando las finanzas, el desarrollo del capital humano y el liderazgo efectivo.
* **Transformación Digital e IA:** Preparado para liderar la adopción tecnológica en las empresas, incorporando **Inteligencia Artificial** y nuevas herramientas bajo enfoques éticos y globales.
* **Analítica y Decisiones Basadas en Datos:** Habilidad para realizar análisis estratégicos complejos y traducir grandes volúmenes de datos en decisiones de negocio de alto impacto.
* **Formulación y Evaluación de Proyectos:** Aptitud para estructurar, evaluar y dirigir proyectos de ingeniería aplicando metodologías rigurosas y sustentadas en la viabilidad técnica y económica.

---

### 💡 Información Complementaria para el Portafolio

#### Enfoque Técnico y Metodológico
* **Enfoque Data-Driven & Business Analytics:** Capacidad para transformar datos brutos en insights estratégicos, desarrollando modelos descriptivos y predictivos para optimizar la toma de decisiones.
* **Metodologías de Mejora Continua:** Aplicación de enfoques como Lean, Six Sigma y gestión de restricciones para la optimización de flujos de valor y eficiencia en procesos.
* **Gestión de Proyectos Operacionales:** Formulación, evaluación técnica-económica y dirección de proyectos bajo metodologías ágiles y tradicionales.

#### Tech Stack & Herramientas de Ingeniería
* **Análisis y Modelamiento de Datos:** Python (Pandas, NumPy, Polars, PySpark), SQL (PostgreSQL), modelamiento de bases de datos relacionales y optimización de consultas.
* **Inteligencia de Negocios y Dashboards:** Diseño y automatización de tableros de control predictivos y KPIs estratégicos para el monitoreo de Supply Chain y mantenimiento.
* **Automatización y Despliegue:** Construcción de MVPs y APIs modernas (FastAPI), control de versiones (Git), y despliegue ágil en entornos en la nube (Cloud/Railway).

#### Enfoque Técnico y Metodológico
El perfil combina la rigurosidad científica de la ingeniería tradicional con las demandas de la industria 4.0:
* **Mentalidad Lean & Agile:** Orientación hacia la reducción de desperdicios, optimización de flujos de valor y adaptabilidad ante el cambio.
* **Business Analytics:** Capacidad no solo de recopilar datos, sino de generar modelos descriptivos y predictivos para la planificación empresarial.

#### Áreas de Impacto Profesional
* Reingeniería y Automatización de Procesos.
* Dirección de Proyectos Tecnológicos y de Innovación.
* Consultoría Estratégica y de Operaciones.
* Gerencia de Logística y Supply Chain.', 'https://postgrados.udd.cl/programas/miis-magister-en-ingenieria-industrial-y-de-sistemas-192133/', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('b4549195-aeeb-4a3b-813d-36b4f9f40e84', '00000000-0000-4000-8000-000000000000', 'Eclass', 'Inglés Profesional — Nivel CEFR B1+ / B2 (Eclass)',
    2022, '# Competencias Lingüísticas

Este nivel certifica una competencia de **Usuario Independiente Avanzado**, lo que me permite interactuar en entornos profesionales, técnicos y multiculturales con fluidez y autonomía, sin requerir supervisión constante.

### Capacidades y Competencias Clave:

* **Comunicación en Entornos Laborales:** Capacidad para participar activamente en reuniones técnicas, presentar informes de gestión, debatir ideas y defender puntos de vista profesionales con claridad.
* **Comprensión de Textos Complejos:** Facultad para comprender las ideas principales de textos abstractos o de carácter técnico, incluyendo manuales, documentación de ingeniería, artículos especializados y especificaciones de proyectos.
* **Fluidez y Espontaneidad:** Habilidad para mantener conversaciones fluidas con hablantes nativos y profesionales de distintas áreas, garantizando que la comunicación sea natural y eficiente en el día a día.
* **Producción de Contenido Escrito:** Capacidad para redactar correspondencia formal, correos corporativos y reportes técnicos detallados, explicando problemas y proponiendo soluciones de forma estructurada.

---

### 🚀 Enfoque Práctico (Ámbito de Aplicación)

*(Nota: Esta sección demuestra cómo aplicas activamente el idioma en tu perfil tecnológico e industrial)*

* **Documentación y Stack Tecnológico:** Lectura e interpretación fluida de documentación técnica oficial, APIs, arquitecturas de software y repositorios de código.
* **Contexto Global de Negocios:** Preparación para interactuar en cadenas de suministro globales, comprender dinámicas de mercados internacionales y colaborar en proyectos o células de trabajo multidisciplinarias con alcance internacional.', '', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('d8c28f62-ee78-4394-8e61-b1aed73b5266', '00000000-0000-4000-8000-000000000000', ' Bootcamp Coding Dojo', 'Full Stack Developer Python — (Black Belt)',
    2021, '# Formación Tecnológica Avanzada

Certificación de **Cinturón Negro (Black Belt)**, la máxima distinción técnica otorgada por Coding Dojo. Este logro acredita un dominio avanzado en el desarrollo de aplicaciones web de extremo a extremo (Full Stack), validado mediante exámenes prácticos de alto rendimiento bajo restricciones de tiempo críticas (desarrollo, pruebas y despliegue de una app funcional en menos de 4 horas).

El programa enfoca su metodología en la autonomía, la resolución de problemas complejos y la adopción de buenas prácticas de ingeniería de software.

### Stack Tecnológico y Competencias Clave:

* **Arquitectura del Backend (Python):** Diseño y construcción de lógicas de servidor robustas, desarrollo de APIs RESTful y gestión de aplicaciones modulares utilizando frameworks líderes como **Django** y **Flask**.
* **Modelamiento de Bases de Datos (SQL):** Diseño de esquemas relacionales eficientes, manipulación avanzada de datos (CRUD), optimización de consultas y uso de ORMs para una integración segura entre la data y el servidor.
* **Desarrollo del Frontend:** Creación de interfaces de usuario dinámicas, interactivas y responsivas utilizando **JavaScript (ES6+)**, manipulación del DOM, integración con APIs del backend, y maquetación moderna con HTML5 y CSS3 (Bootstrap/Tailwind).
* **Ciclo de Vida del Desarrollo (SDLC):** Dominio en el control de versiones con **Git/GitHub**, depuración rigurosa de errores (debugging) y estrategias de despliegue en entornos de producción en la nube.

---

### 🚀 Capacidades Profesionales Demostradas

*(Nota: Esto traduce el "Black Belt" al lenguaje que buscan las células de desarrollo ágil y startups)*

* **Desarrollo Ágil Bajo Presión:** Capacidad probada para priorizar requerimientos, estructurar arquitecturas limpias y entregar productos mínimos viables (MVPs) funcionales en tiempos extremadamente reducidos.
* **Pensamiento Algorítmico y Escalabilidad:** Enfoque en la escritura de código limpio, mantenible y estructurado, facilitando el trabajo en células ágiles de desarrollo y la integración con tecnologías emergentes.', '', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('6148554e-9842-4541-a5b8-c90ba20656ad', '00000000-0000-4000-8000-000000000000', 'Microsoft Certified', 'Certificación PL-900: Fundamentos de Microsoft Power Platform',
    2021, '# Certificaciones Oficiales

Certificación oficial emitida por **Microsoft** que valida el conocimiento fundamental y las capacidades técnicas para transformar procesos de negocio utilizando el ecosistema de **Power Platform**. Acredita la competencia para diseñar soluciones de bajo código (Low-Code), automatizar flujos de trabajo operativos, analizar datos para la toma de decisiones y construir aplicaciones empresariales ágiles.

Esta credencial demuestra la habilidad para acelerar la transformación digital dentro de las organizaciones, reduciendo los tiempos de desarrollo y mejorando la eficiencia operativa.

### Componentes Clave y Capacidades Validadas:

* **Análisis de Datos con Power BI:** Capacidad para conectar diversas fuentes de datos, modelar la información y crear tableros de control (Dashboards) interactivos e intuitivos que faciliten el monitoreo de KPIs y la toma de decisiones estratégicas.
* **Automatización de Procesos con Power Automate:** Habilidad para diseñar y desplegar flujos de trabajo automatizados (automatización de tareas repetitivas, aprobaciones y alertas), integrando de forma nativa aplicaciones y servicios en la nube.
* **Desarrollo de Aplicaciones con Power Apps:** Competencia para crear aplicaciones empresariales personalizadas (Canvas y Model-Driven Apps) orientadas a resolver necesidades operativas específicas y mejorar la productividad de los equipos de trabajo.
* **Gestión de Datos con Microsoft Dataverse:** Comprensión de la arquitectura de datos segura y escalable de Microsoft, permitiendo almacenar y gestionar de manera eficiente los datos utilizados por las aplicaciones de la organización.
* **Eficiencia Organizacional con Copilot Studio:** Entendimiento de las capacidades básicas de IA para la creación de agentes y chatbots que optimicen la interacción y el soporte interno o externo.

---

### 🚀 Valor Agregado para el Perfil

*(Nota: Esto resalta el impacto estratégico de la certificación ante directores de tecnología u operaciones)*

* **Agilidad en la Transformación Digital:** Capacidad para actuar como un "Citizen Developer" o integrador técnico, implementando soluciones rápidas y eficientes que complementan el desarrollo de software tradicional.
* **Sinergia Corporativa:** Preparación para diseñar soluciones que se integran de forma nativa con el entorno Microsoft 365, Azure y bases de datos relacionales, garantizando la escalabilidad y seguridad de la información corporativa.', 'https://www.credly.com/badges/e99c1f84-c665-4d45-afe8-5998c9783fd2/linked_in', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('c485f6e1-53e6-44fe-b746-6a4bc2aaf9d5', '00000000-0000-4000-8000-000000000000', 'Google Cloud Certified', 'Prepare Data for ML APIs on Google Cloud Skill Badge',
    2025, '# Certificaciones y Skill Badges

Insignia técnica (*Skill Badge*) emitida por **Google Cloud** que demuestra la capacidad práctica y validada para ejecutar laboratorios de rendimiento avanzado en ingeniería de datos aplicada a la Inteligencia Artificial. Acredita el dominio técnico en la limpieza, transformación, análisis y preparación de grandes volúmenes de datos (*Data Preparation*) utilizando la infraestructura de **Google Cloud Platform (GCP)** para alimentar de forma óptima modelos de Machine Learning (ML).

Esta credencial certifica que el profesional cuenta con las competencias necesarias para estructurar flujos de datos (*data pipelines*) eficientes, garantizando el rendimiento de las soluciones analíticas modernas.

### Tecnologías Clave y Capacidades Validadas:

* **Análisis de Datos a Gran Escala con BigQuery:** Dominio en el uso del almacén de datos empresarial de Google para realizar consultas SQL analíticas avanzadas, explorar conjuntos de datos masivos y estructurar la data antes de su procesamiento.
* **Preparación Visual de Datos con Dataprep:** Habilidad para explorar, limpiar y transformar visualmente datos estructurados y no estructurados de manera ágil, identificando anomalías o valores nulos antes de su integración.
* **Integración y Consumo de APIs de Machine Learning:** Comprensión práctica de cómo conectar la data preparada con las APIs nativas de GCP (como *Cloud Vision*, *Natural Language*, *Speech-to-Text* y *Translation*) para extraer insights automatizados de alto valor.
* **Orquestación de Pipelines en la Nube:** Capacidad para mover datos de forma segura entre el almacenamiento en la nube (**Cloud Storage**) y los motores de procesamiento, asegurando flujos continuos y limpios.

---

### 🚀 Valor Agregado para el Perfil

*(Nota: Esto resalta cómo este logro técnico potencia tus habilidades como Ingeniero y Desarrollador)*

* **Fundación para MLOps:** Respaldo técnico que demuestra habilidades esenciales en la fase más crítica de cualquier proyecto de Inteligencia Artificial: la calidad y el preprocesamiento de los datos raw.
* **Versatilidad Cloud (Multicloud):** Evidencia una capacidad sólida para operar e integrar soluciones de datos tanto en arquitecturas de Microsoft Azure como en flujos analíticos de Google Cloud, adaptándose con agilidad a las necesidades de infraestructura de cualquier organización.', 'https://www.credly.com/earner/earned/badge/352c631b-71ca-4415-9785-e0b68e6fe62d', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('e53c0d07-6985-44d2-8fd3-69fdcefe06d2', '00000000-0000-4000-8000-000000000000', 'Cisco Networking Academy', 'Python Essentials 1',
    2025, '# Formación y Fundamentos Tecnológicos

Certificación oficial emitida por **Cisco** que valida el conocimiento fundamental de la programación de computadoras utilizando el lenguaje **Python**. Esta credencial acredita una base sólida en el diseño algorítmico, la lógica de programación y la resolución de problemas, asegurando que el código escrito siga los estándares de la industria en cuanto a legibilidad, estructura y eficiencia.

El programa establece los pilares lógicos necesarios para avanzar con éxito hacia el desarrollo de software complejo, la ingeniería de datos y la automatización.

### Competencias Clave y Capacidades Validadas:

* **Estructuras de Control y Lógica:** Dominio en el diseño de algoritmos utilizando ejecución condicional (`if-else`), bucles (`while`, `for`) y control de flujos de datos.
* **Tipos de Datos y Operaciones:** Comprensión profunda del sistema de tipos de Python (enteros, flotantes, strings, booleanos) y operadores lógicos, aritméticos y de asignación.
* **Colecciones y Estructuras de Datos Nativas:** Manipulación fluida y eficiente de colecciones de datos esenciales como **listas, tuplas, diccionarios y sets**, comprendiendo sus casos de uso específicos y optimización.
* **Modularización mediante Funciones:** Capacidad para descomponer problemas complejos en componentes más pequeños y reutilizables mediante la definición de funciones, manejo de parámetros, argumentos y ámbitos de variables (*scopes*).
* **Entornos de Desarrollo y Buenas Prácticas:** Familiaridad con el proceso de compilación/interpretación, ejecución de scripts en consola, depuración básica de errores sintácticos y semánticos, y adherencia a las convenciones de estilo de Python (PEP 8).

---

### 🚀 Sinergia con el Stack Profesional

*(Nota: Esto conecta los fundamentos de Cisco con tus capacidades avanzadas en datos y desarrollo)*

* **Código Limpio y Mantenible:** Garantía de que el desarrollo posterior con frameworks avanzados (como FastAPI, Django o Flask) o librerías de analítica de datos (Pandas, Polars, PySpark) se construye sobre una base lógica limpia, estructurada y sin vicios de programación.
* **Pensamiento Analítico de Ingeniería:** Respaldo de una de las academias tecnológicas más prestigiosas del mundo (Cisco), demostrando un enfoque metódico para traducir procesos lógicos de negocio en código de computadora eficiente.', 'https://www.credly.com/earner/earned/badge/72487490-d99c-451d-8805-3a509473bcc4', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('15cd0c88-24ac-4d17-bb50-c1c4ecc57dc1', '00000000-0000-4000-8000-000000000000', 'EY Certification', 'EY Artificial Intelligence - AI Engineering - Bronze Learning (2023)',
    2023, '# Certificaciones Corporativas Internacionales

Credencial internacional emitida por **Ernst & Young (EY)** que valida competencias técnicas y metodológicas esenciales en la **Ingeniería de Inteligencia Artificial (AI Engineering)**. Este distintivo certifica la adquisición y comprensión profunda de arquitecturas de IA, flujos de desarrollo de modelos y las mejores prácticas de la industria para integrar capacidades cognitivas y de automatización avanzada en entornos empresariales globales.

Representa la base técnica necesaria para conectar los datos organizacionales con sistemas inteligentes que optimicen los procesos y la toma de decisiones.

### Competencias Clave y Capacidades Validadas:

* **Fundamentos de Ingeniería de IA:** Comprensión del ciclo de vida de un sistema de Inteligencia Artificial, abarcando desde la concepción del problema y la preparación del pipeline de datos, hasta el entrenamiento, evaluación y monitoreo de modelos.
* **Aprendizaje Automático y Redes Neuronales:** Conocimiento en la selección y aplicación de algoritmos de Machine Learning (supervisado y no supervisado) y conceptos esenciales de Deep Learning para resolver problemas complejos de predicción, clasificación y optimización.
* **Procesamiento de Datos para Inteligencia Artificial:** Capacidad para estructurar flujos de datos limpios, consistentes y de alta calidad, reconociendo que la preparación de los datos (*Data Preparation*) es el pilar del éxito en cualquier modelo de ingeniería de IA.
* **IA Responsable y Ética Tecnológica:** Comprensión de los marcos normativos, mitigación de sesgos en los datos, explicabilidad de los modelos y gobernanza, garantizando un despliegue ético y seguro de las soluciones tecnológicas a escala corporativa.

---

### 🚀 Impacto Estratégico en el Perfil de Ingeniería

*(Nota: Esto conecta el badge con tus capacidades como desarrollador e ingeniero industrial y de sistemas)*

* **Visión de Vanguardia Tecnológica (Iniciada en 2023):** Demuestra un compromiso temprano y sostenido con la adopción de las olas tecnológicas más disruptivas, permitiéndote liderar iniciativas de transformación digital orientadas a la automatización inteligente.
* **Sinergia con el Stack de Desarrollo:** Respalda de forma corporativa tu capacidad para construir el software que sirve de infraestructura a estas herramientas (como APIs eficientes en FastAPI), asegurando que la IA se traduzca en una solución productiva, estable y de alto valor para el negocio.', 'https://www.credly.com/badges/8108f28e-33aa-4437-b397-72bb95269a90', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('f94f3c83-4d6f-4048-9baf-7d21901b9cf1', '00000000-0000-4000-8000-000000000000', 'Microsoft Certified', 'Certificación DP-900: Fundamentos de Datos en Microsoft Azure',
    2023, '# Certificaciones Oficiales

Certificación oficial emitida por **Microsoft** que valida el conocimiento técnico fundamental en conceptos de datos y su implementación utilizando los servicios de computación en la nube de **Microsoft Azure**. Esta credencial acredita la comprensión profunda de cómo se procesan, almacenan, aseguran y analizan los datos en entornos *Cloud* e híbridos.

Demuestra una base sólida para colaborar con equipos de Ingeniería de Datos, Ciencia de Datos y Business Intelligence, garantizando que las soluciones se diseñen bajo estándares modernos de la industria.

### Componentes Clave y Capacidades Validadas:

* **Conceptos de Datos e Infraestructura Nube:** Comprensión clara de los pilares de datos modernos: datos estructurados, semiestructurados (JSON/XML) y no estructurados, además de los conceptos clave de procesamiento analítico (OLAP) y transaccional (OLTP).
* **Bases de Datos Relacionales en Azure:** Conocimiento en el aprovisionamiento, configuración y consulta de servicios de datos relacionales en la nube (como Azure SQL Database o Azure Database for PostgreSQL), asegurando la integridad y disponibilidad de la data.
* **Soluciones de Datos No Relacionales:** Entendimiento de los casos de uso y la estructura de repositorios no relacionales (NoSQL), almacenamiento de archivos y tablas a gran escala (Azure Blob Storage, Azure Cosmos DB).
* **Arquitecturas de Analítica Avanzada y Big Data:** Comprensión de los componentes esenciales de un almacén de datos moderno (Data Warehouse) y lagos de datos (Data Lakes), utilizando servicios como Azure Synapse Analytics, Azure Databricks y Azure Data Factory para flujos de ingesta (ETL/ELT).

---

### 🚀 Valor Agregado para el Perfil

*(Nota: Esto conecta la certificación en la nube con tus capacidades en ingeniería industrial y de sistemas)*

* **Arquitectura de Datos Escalable:** Capacidad para evaluar y proponer la infraestructura de datos más eficiente para proyectos empresariales, optimizando costos operativos de cómputo y almacenamiento en la nube.
* **Sinergia con el Stack Técnico:** Respaldo oficial para el diseño y conexión de bases de datos relacionales robustas, garantizando que el backend de las aplicaciones y los tableros analíticos se alimenten de fuentes de datos estables, seguras y de alto rendimiento.', 'https://learn.microsoft.com/en-us/users/jaimecampillay-2360/credentials/b072890bc8305406?ref=https%3A%2F%2Fwww.linkedin.com%2F', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('eb32e5d6-e7a0-4da6-8f5c-d1279343997a', '00000000-0000-4000-8000-000000000000', 'EY Certification', 'EY Artificial Intelligence - AI Engineering - Bronze Learning (2023)',
    2023, '# Certificaciones Corporativas Internacionales

Credencial internacional emitida por **Ernst & Young (EY)** que valida competencias técnicas y metodológicas esenciales en la **Ingeniería de Inteligencia Artificial (AI Engineering)**. Este distintivo certifica la adquisición y comprensión profunda de arquitecturas de IA, flujos de desarrollo de modelos y las mejores prácticas de la industria para integrar capacidades cognitivas y de automatización avanzada en entornos empresariales globales.

Representa la base técnica necesaria para conectar los datos organizacionales con sistemas inteligentes que optimicen los procesos y la toma de decisiones.

### Competencias Clave y Capacidades Validadas:

* **Fundamentos de Ingeniería de IA:** Comprensión del ciclo de vida de un sistema de Inteligencia Artificial, abarcando desde la concepción del problema y la preparación del pipeline de datos, hasta el entrenamiento, evaluación y monitoreo de modelos.
* **Aprendizaje Automático y Redes Neuronales:** Conocimiento en la selección y aplicación de algoritmos de Machine Learning (supervisado y no supervisado) y conceptos esenciales de Deep Learning para resolver problemas complejos de predicción, clasificación y optimización.
* **Procesamiento de Datos para Inteligencia Artificial:** Capacidad para estructurar flujos de datos limpios, consistentes y de alta calidad, reconociendo que la preparación de los datos (*Data Preparation*) es el pilar del éxito en cualquier modelo de ingeniería de IA.
* **IA Responsable y Ética Tecnológica:** Comprensión de los marcos normativos, mitigación de sesgos en los datos, explicabilidad de los modelos y gobernanza, garantizando un despliegue ético y seguro de las soluciones tecnológicas a escala corporativa.

---

### 🚀 Impacto Estratégico en el Perfil de Ingeniería

*(Nota: Esto conecta el badge con tus capacidades como desarrollador e ingeniero industrial y de sistemas)*

* **Visión de Vanguardia Tecnológica (Iniciada en 2023):** Demuestra un compromiso temprano y sostenido con la adopción de las olas tecnológicas más disruptivas, permitiéndote liderar iniciativas de transformación digital orientadas a la automatización inteligente.
* **Sinergia con el Stack de Desarrollo:** Respalda de forma corporativa tu capacidad para construir el software que sirve de infraestructura a estas herramientas (como APIs eficientes en FastAPI), asegurando que la IA se traduzca en una solución productiva, estable y de alto valor para el negocio.', 'https://www.credly.com/badges/8108f28e-33aa-4437-b397-72bb95269a90', true);


INSERT INTO oppy.estudios 
    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
    VALUES ('8501900c-d10d-447a-9145-56ec4105cd4f', '00000000-0000-4000-8000-000000000000', 'Cisco Networking Academy', 'Python Essentials 2',
    2025, '# Formación y Fundamentos Tecnológicos

Certificación avanzada emitida por **Cisco** que valida el dominio de conceptos complejos y técnicas profesionales de desarrollo en **Python**. Esta credencial acredita la capacidad para diseñar y construir aplicaciones bajo el paradigma de la **Programación Orientada a Objetos (POO)**, gestionar paquetes y módulos a nivel de sistema, procesar archivos y flujos de datos, y aplicar estrategias avanzadas de manejo de excepciones.

Demuestra un nivel de preparación óptimo para abordar el desarrollo de software escalable, automatizaciones avanzadas e ingeniería de datos con estándares profesionales de la industria.

### Competencias Clave y Capacidades Validadas:

* **Programación Orientada a Objetos (POO):** Comprensión profunda e implementación de clases, objetos, propiedades, métodos, encapsulamiento, herencia (simple y múltiple) y polimorfismo para estructurar código modular y altamente reutilizable.
* **Módulos y Paquetes a Gran Escala:** Capacidad para utilizar, configurar y crear módulos y paquetes personalizados de Python, además del dominio en la gestión de librerías externas utilizando el ecosistema `pip`.
* **Procesamiento Avanzado de Strings y Archivos:** Manipulación experta de flujos de texto (Strings), métodos de formateo y operaciones de lectura/escritura de archivos en el sistema de almacenamiento local, garantizando la persistencia y el procesamiento eficiente de datos.
* **Gestión Profesional de Excepciones:** Diseño de bloques robustos de control de errores (`try-except-else-finally`) y creación de excepciones personalizadas para asegurar la estabilidad, resiliencia y correcto *debugging* de las aplicaciones ante fallos en tiempo de ejecución.
* **Uso de Generadores, Iteradores y Closures:** Comprensión de herramientas avanzadas de Python que permiten optimizar el uso de memoria y el rendimiento del código al procesar flujos continuos de datos.

---

### 🚀 Impacto en el Stack de Ingeniería

*(Nota: Esto conecta el nivel avanzado de Cisco con tus habilidades en ciencia de datos y desarrollo Full Stack)*

* **Arquitecturas Limpias y Escalables:** Garantiza la base técnica necesaria para entender las entrañas de los frameworks modernos de Python (como los modelos y esquemas de *Pydantic* en FastAPI o los ORM en bases de datos), permitiéndote personalizarlos y extenderlos eficientemente.
* **Código de Calidad Corporativa:** Evidencia que tu software está diseñado para fallar con elegancia y mantenerse fácilmente en el tiempo, cumpliendo con los requisitos rigurosos que exigen los equipos de desarrollo y las células ágiles de ingeniería.', 'https://www.credly.com/earner/earned/badge/9dfbcca0-0dfb-4f86-8f41-bcd07de6f385', true);


INSERT INTO oppy.reconocimientos 
    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
    VALUES ('096e2647-02c6-4a46-bf89-e37b393448a4', '00000000-0000-4000-8000-000000000000', 'PREMIO', 'Ovación EY', 'EY',
    '2021', 'Galardonado con la distinción interna "Ovación", un reconocimiento otorgado por la plana directiva de EY a profesionales que demuestran un desempeño excepcional, liderazgo y un compromiso que supera los estándares habituales del cargo. Este hito destaca mi capacidad para entregar soluciones de alta calidad en entornos de alta exigencia, colaborar efectivamente en equipos multidisciplinarios e impulsar la innovación en los proyectos asignados.', '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('62aa8a4a-71e0-4e2f-b8df-19504a56a9f3', '00000000-0000-4000-8000-000000000000', 'Plataforma de Analítica Industrial y Confiabilidad Predictiva', 'Plataforma Cloud-Native orientada a Centros de Control Remoto que automatiza procesos ETL masivos de telemetría, combinando visualización de datos interactiva e Inteligencia Artificial para el soporte en la toma de decisiones estratégicas.',
    'Este proyecto aborda los desafíos analíticos de flotas y maquinaria industrial pesada (orientado a industrias como la minería o manufactura). Su propósito es encontrar soluciones a problemas operacionales mediante el modelado, limpieza y visualización de datos (Telemetría IoT). Actúa como una herramienta centralizada para transformar datos crudos en estrategias accionables, reduciendo el *downtime* y facilitando un monitoreo continuo basado en métricas clave de confiabilidad.

---

## 🚀 Highlights del Proyecto (Orientado a Data Engineering & Analytics)

- **Diseño y Desarrollo de Procesos ETL:** Canalización, limpieza y procesamiento automatizado de **+870,000 registros** históricos de telemetría y eventos utilizando **Polars** y **PyArrow**, garantizando la integridad, calidad y alta disponibilidad para análisis.
- **Analítica Avanzada y KPIs Estratégicos:** Desarrollo de modelos analíticos descriptivos para el cálculo en tiempo real de indicadores críticos de confiabilidad, tales como **MTBF** (Tiempo Medio Entre Fallas) y **MTTR** (Tiempo Medio de Reparación).
- **Inteligencia Artificial y Modelos Prescriptivos:** Integración profunda con modelos generativos (**Gemini 3 Flash**) que actúa como un "Analista Virtual". Permite a los operadores realizar consultas complejas sobre la flota, generando diagnósticos automatizados y recomendaciones (prescriptivas) frente a anomalías detectadas.
- **Monitoreo Operacional de Alto Desempeño:** Dashboard interactivo construido con **Dash/Plotly** que permite la supervisión de señales de IoT (Vibración, Voltaje, Presión) y el registro de eventos en tiempo real, ideal para un *Trainee Specialist* o Especialista de Centro Remoto.
- **UX/UI Dinámica (Dark Mode Integral):** Aplicación de interfaces modernas con adaptación de temas dinámicos (Claro/Oscuro) que se sincronizan desde el contenedor HTML hasta el renderizado gráfico avanzado de Plotly y DataTables.
- **DevSecOps y Seguridad de Datos:** Aplicación de mejores prácticas de ciberseguridad, incluyendo el *hardening* de la API con **FastAPI**, inyección de cabeceras de seguridad estrictas (HSTS, Anti-Clickjacking), prevención contra fuga de información (*Stack Traces*) e integración CORS segura.
- **Arquitectura Híbrida y Cloud Native:** Desarrollo e integración nativa de tecnologías desplegadas en contenedores **Docker**, con bases de datos relacionales manejadas mediante **SQLAlchemy 2.0** y hospedadas en la nube (**PostgreSQL Serverless** / Railway).', '["FastAPI", "Polars", "PostgreSQL", "Cloud Computing", "Dash", "Plotly", "AI/LLM", "ETL", "Docker", "Git"]'::json, '2024-01-01', 'https://github.com/jcampillay8/Predictive_Maintenance.git', 'https://predictivemaintenance-production.up.railway.app/dashboard/', '{"Nivel de Ciberseguridad Aplicado": "Hardening Estricto (Protecci\u00f3n OWASP B\u00e1sica)", "M\u00e9tricas de Confiabilidad Target": "Aumento del MTBF y reducci\u00f3n del MTTR", "Volumen de Datos Procesados (ETL)": "+870,000 registros de telemetr\u00eda", "Rendimiento de Consultas Anal\u00edticas": "< 100ms utilizando Polars"}'::json, '["Data Engineering", "Predictive Maintenance", "ETL", "Data Analytics", "Artificial Intelligence", "IoT", "Centro de Control Remoto", "Dashboard", "Data Pipeline"]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('6f64b94f-983b-44b4-9d53-47500a8e50e6', '00000000-0000-4000-8000-000000000000', 'Consultoría Estratégica de Migración Cloud y Arquitectura Híbrida de Alta Disponibilidad', '**Consultoría estratégica para Redbanc** enfocada en la hoja de ruta para migrar su infraestructura crítica a un modelo de Nube Híbrida. Evalúa riesgos, seguridad y *FinOps*, definiendo una arquitectura basada en Docker y Kubernetes para asegurar la resiliencia del sistema interbancario.',
    '## 📋 Contexto y Desafío Operacional

Como actor clave del ecosistema financiero chileno, **Redbanc** procesa de forma segura y masiva las transacciones electrónicas e interconexiones de cajeros automáticos de la banca nacional, operando una infraestructura crítica para la continuidad del sistema financiero del país.

Ante las nuevas demandas del mercado y la necesidad de mayor adaptabilidad tecnológica, surgió el desafío de modernizar una infraestructura tradicional **On-Premise**, reduciendo la rigidez de servidores locales y aumentando la capacidad de responder eficientemente a cargas transaccionales variables.

El principal reto de esta asesoría estratégica consistía en equilibrar las ventajas de la computación en la nube —flexibilidad, escalabilidad elástica y optimización de costos operativos— con el cumplimiento estricto de las exigentes normativas bancarias relacionadas con:

- Seguridad de la información  
- Auditoría y trazabilidad  
- Gobernanza de datos  
- Alta disponibilidad operacional  

Era fundamental diseñar una transición tecnológica que eliminara riesgos de interrupción en un servicio interbancario considerado crítico para la estabilidad económica nacional.

---

## 🛠️ Solución Implementada (La Acción)

Lideré el análisis y estructuración de una **Cloud Strategy** orientada a conectar viabilidad técnica, eficiencia financiera y cumplimiento regulatorio, construyendo un marco de referencia integral para la toma de decisiones.

### ☁️ Análisis comparativo de proveedores Cloud mediante Power BI

Diseñé y desarrollé un **dashboard interactivo en Power BI** utilizado como herramienta central para la toma de decisiones estratégicas.

La plataforma consolidó y parametrizó información crítica para comparar de manera transversal a los principales proveedores de nube:

- Google Cloud Platform (GCP)  
- Amazon Web Services (AWS)  
- Oracle Cloud Infrastructure (OCI)  
- Microsoft Azure  

El dashboard permitió evaluar visualmente y en tiempo real:

- Capacidades técnicas  
- Escalabilidad y desempeño  
- Costos proyectados  
- Riesgos regulatorios  
- Seguridad y cumplimiento normativo  
- Fortalezas y debilidades arquitectónicas  

Esto permitió a la gerencia construir una evaluación objetiva y basada en datos para determinar la alternativa tecnológica más conveniente para Redbanc.

---

### 🏗️ Diseño de estrategia de nube híbrida (Hybrid Cloud Architecture)

Definí una arquitectura de migración basada en un enfoque **Hybrid Cloud**, identificada como la alternativa óptima para equilibrar seguridad, escalabilidad y cumplimiento regulatorio.

El diseño propuso:

- **Nube privada/local** para almacenamiento de datos altamente sensibles y procesos regulatorios críticos  
- **Nube pública** para absorber cargas variables y escalar dinámicamente ante peaks transaccionales  

Este enfoque permitía maximizar elasticidad operativa sin comprometer integridad ni confidencialidad de los datos financieros.

---

### 🐳 Modernización mediante contenedores (Docker & Kubernetes)

Incorporé al diseño arquitectónico el uso de tecnologías de contenedorización y orquestación empresarial mediante **Docker** y **Kubernetes**.

Estas tecnologías fueron definidas como estándar técnico para:

- Garantizar portabilidad entre entornos On-Premise y Cloud  
- Facilitar despliegues ágiles y consistentes  
- Mejorar tolerancia a fallos y resiliencia operativa  
- Escalar aplicaciones desacopladas según demanda transaccional  
- Reducir dependencia de infraestructura física tradicional  

---

### 📊 Evaluación multidimensional (FinOps & Ciberseguridad)

Estructuré el caso de negocio evaluando la transformación tecnológica desde una perspectiva integral de **FinOps, arquitectura empresarial y seguridad**.

El análisis consideró:

- Modelos de costos (**CapEx vs. OpEx**)  
- Reducción proyectada de costos de infraestructura física  
- Requerimientos de seguridad perimetral  
- Integridad y continuidad operacional  
- Protección de transacciones financieras críticas  

Esto permitió construir una propuesta técnicamente viable, financieramente sustentable y alineada con los estándares de seguridad exigidos por la industria bancaria.', '["Cloud Strategy", "Cloud Migration Architecture", "Kubernetes", "Docker", "Hybrid Cloud Ecosystems", "FinOps (Cost Optimization)", "IT Governance", "Risk & Compliance (GRC)", "Infrastructure Modernization", "Power BI\""]'::json, '2024-01-01', '', '', '{"Estrategia & Gobernanza": {"Foco Regulatorio": "Gobernanza de Datos Sensibles e Integridad Financiera", "Modelo de Enfoque": "Cloud Strategy (Estrategia de Nube Corp)", "Topolog\u00eda Dise\u00f1ada": "Arquitectura de Nube H\u00edbrida (P\u00fablica + Privada)", "Paradigmas de Despliegue": "Contenedorizaci\u00f3n y Orquestaci\u00f3n Microservicios"}, "Componentes Tecnol\u00f3gicos": {"Gesti\u00f3n de Cargas": "Enrutamiento din\u00e1mico seg\u00fan criticidad del Payload", "Infraestructura Origen": "Servidores Locales Tradicionales On-Premise", "Tecnolog\u00eda de Empaquetado": "Docker (Im\u00e1genes livianas y portables)", "Plataforma de Orquestaci\u00f3n": "Kubernetes (Estrategias de Auto-scaling y Self-healing)"}, "Impacto & Valor de Negocio": {"Ventaja Competitiva": "Aceleraci\u00f3n del Time-to-Market para responder a las necesidades cambiantes del mercado financiero", "Eficiencia Financiera": "Reducci\u00f3n proyectada de costos operativos e inversi\u00f3n en infraestructura f\u00edsica (OpEx Optimization)", "Flexibilidad Operativa": "Escalabilidad el\u00e1stica de recursos de c\u00f3mputo ante fluctuaciones de demanda", "Objetivo de Disponibilidad": "Mitigaci\u00f3n del riesgo de downtime en la red interbancaria"}}'::json, '["Estrategia Cloud", "Arquitectura H\u00edbrida", "Contenedores", "Redbanc", "Continuidad Operativa", "Transformaci\u00f3n Digital", "Consultor\u00eda Tecnol\u00f3gica", "FinOps", "Alta Disponibilidad", "Infraestructura Bancaria."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('2bd3ebc5-e3fb-45db-9d0b-d1806d448e14', '00000000-0000-4000-8000-000000000000', 'ReportWorks — Sistema Automatizado de Captura y Reportabilidad en Terreno', 'Aplicación móvil Android y motor de automatización low-code** que transformó radicalmente el control operacional en alta cordillera. Automatiza la captura de datos en terreno de 9 a 15 células de trabajo simultáneas, eliminando reportes en papel y formatos corruptos de Excel mediante la ingesta, depuración e integración asíncrona de datos en un reporte gerencial unificado en tiempo real.',
    '# 🚀 Caso de Éxito: ReportWorks (Techint)

**Empresa / Cliente:** Techint Ingeniería y Construcción | Proyecto Mina Los Bronces (Anglo American Sur)  
**Rol:** Ingeniero Analista en Programación y Control de Gestión *(Creador y Desarrollador del Proyecto)*  
**Periodo:** 2019 – 2020  
**Stack Tecnológico:** MIT App Inventor (Android), Excel Avanzado (VBA / Macros), Google Apps Script, Google Sheets

---

## 📋 Contexto y Desafío Operacional (La Problemática)

Durante el macroproyecto de reparación y reemplazo de cañerías de transporte de minerales en Mina Los Bronces, múltiples células de trabajo operaban de manera simultánea a lo largo de varios kilómetros de alta cordillera. Las actividades incluían procesos críticos y heterogéneos tales como:

- Reconocimiento de terreno  
- Movimiento de tierras  
- Transporte de materiales  
- Soldadura y doblado de cañerías  
- Descenso de tubos mediante maquinaria pesada (*sidebooms*)  
- Controles de calidad operacionales  

Para mantener el control diario de las operaciones, cada frente de trabajo contaba con un **“Apuntador”**, responsable de registrar:

- Actividades ejecutadas durante la jornada  
- Asistencia del personal  
- Uso de maquinaria pesada  
- Consumo de combustible e insumos operacionales  

### El problema de gestión de datos

Cada día, el área de **Control de Gestión** recibía entre **9 y 15 reportes independientes** que debían consolidarse manualmente en un único informe ejecutivo para la gerencia de obra.

El proceso presentaba dos cuellos de botella críticos:

#### 1. Datos inconsistentes y estructuras destruidas

Los apuntadores trabajaban con planillas libres de Excel que frecuentemente:

- Modificaban tamaños de celdas  
- Fusionaban filas o columnas de manera inconsistente  
- Alteraban nomenclaturas y estructuras del reporte  

Esto impedía cualquier posibilidad de consolidación automatizada y generaba una alta carga de trabajo manual.

#### 2. Brecha digital en alta cordillera

En múltiples zonas sin conectividad a internet, los reportes eran completados manualmente en papel.

Posteriormente, el equipo administrativo debía reconstruir la información desde:

- Fotografías de baja calidad  
- Registros manuscritos difíciles de interpretar  

Esto provocaba extensas jornadas de transcripción, retrasos operacionales y un alto riesgo de error humano.

---

## 🛠️ Solución Implementada (La Acción)

Aprovechando conocimientos adquiridos durante mi formación de postgrado, diseñé y desarrollé **ReportWorks**, una solución integral de extremo a extremo que combinó movilidad, automatización local y consolidación inteligente de datos.

### 📱 Desarrollo móvil para captura en terreno (Android)

Construí una aplicación móvil utilizando **MIT App Inventor**, orientada al uso directo por los apuntadores en terreno.

La solución incorporó:

- Persistencia local de datos  
- Memoria de equipos de trabajo y maquinaria asignada  
- Autocompletado de variables repetitivas  

Esto permitió automatizar aproximadamente el **80% del llenado del reporte**, dejando solo variables dinámicas para edición manual, tales como:

- Avances diarios  
- Horas Hombre (HH)  
- Metros cúbicos procesados  

---

### 📊 Estandarización mediante reportes inteligentes en Excel (VBA)

Para garantizar interoperabilidad incluso sin acceso a internet, la aplicación exportaba automáticamente información estructurada hacia reportes Excel individuales.

Cada planilla incluía **macros VBA embebidas** responsables de:

- Validar consistencia de datos  
- Bloquear celdas críticas para evitar corrupción de formatos  
- Estandarizar estructura documental  
- Generar automáticamente el reporte diario local de cada frente de trabajo  

Esto eliminó por completo los errores derivados de modificaciones accidentales de formato.

---

### ⚙️ Motor de consolidación automatizada (Excel VBA + Google Apps Script)

Desarrollé un motor centralizado de consolidación construido en **Excel VBA** conectado con **Google Apps Script**.

Una vez recibidos los reportes independientes:

- El sistema abría automáticamente múltiples archivos Excel  
- Extraía datos estructurados de forma automatizada  
- Depuraba inconsistencias y validaba integridad  
- Consolidaba toda la operación en una única base de datos operativa  

El resultado era un informe gerencial centralizado generado automáticamente desde múltiples frentes de trabajo distribuidos en alta cordillera.

---

## 🚀 Resultados e Impacto (KPIs)

La implementación de **ReportWorks** generó beneficios inmediatos tanto para operaciones en terreno como para la toma de decisiones ejecutiva.

### ⏱️ Eficiencia en consolidación

El tiempo de construcción del reporte gerencial pasó de **horas de transcripción manual** a una ejecución prácticamente instantánea mediante automatización.

### ⚡ Velocidad de entrega

Los informes ejecutivos comenzaron a estar disponibles de forma significativamente más rápida, permitiendo una reacción operativa más ágil frente a desviaciones en obra.

### ✅ Calidad e integridad del dato

Se eliminó prácticamente el error humano por transcripción y se erradicó la corrupción de formatos Excel gracias a validaciones automáticas y bloqueo estructural mediante macros.

### 👷 Optimización operacional en terreno

Los apuntadores redujeron drásticamente el tiempo administrativo invertido al finalizar sus jornadas, enfocándose más en supervisión y menos en tareas burocráticas.

---

## 💡 Hito de Inflexión Profesional

El impacto tangible de **ReportWorks** marcó un punto de inflexión en mi desarrollo profesional.

Ver cómo automatización, lógica computacional y unas pocas líneas de código podían transformar la operación de una obra minera de gran escala despertó mi interés profundo por la ingeniería de software y la analítica aplicada.

Este proyecto representó el inicio de mi transición hacia el desarrollo de sistemas, automatización avanzada, ingeniería de datos y construcción de soluciones tecnológicas orientadas a resolver problemas reales de negocio.', '["MIT App Inventor", "Android SDK", "Google Apps Script", "Google Sheets", "Excel Macros", "JavaScript (V8 Engine)", "JSON", "Local Storage/Persistence", "Excel", "Macros"]'::json, '2024-01-01', '', '', '{"Tecnolog\u00eda": {"Motor Backend": "Google Apps Script (JavaScript V8)", "Plataforma Mobile": "Android (MIT App Inventor)", "Persistencia Local": "Memoria del dispositivo (Estructuras de datos nativas)", "Almacenamiento Central": "Google Sheets"}, "Rendimiento & Impacto": {"Disponibilidad en terreno": "100% offline (llenado sin cobertura en alta cordillera)", "Estructura de datos corruptas": "0% (bloqueo total de alteraciones de formato Excel)", "Velocidad de entrega a gerencia": "Optimizaci\u00f3n dr\u00e1stica para toma de decisiones diaria", "Tasa de error por transcripci\u00f3n": "0% (eliminaci\u00f3n de digitaci\u00f3n manual de datos)", "Tiempo de procesamiento de reportes": "Reducci\u00f3n de horas a consolidaci\u00f3n casi instant\u00e1nea"}, "Operaciones & Cobertura": {"Fuentes de datos unificadas": "Formatos digitales estandarizados y transcripci\u00f3n de papel obsoleta", "Fases del proyecto cubiertas": "Reconocimiento, movimiento de tierras, transporte, doblado, soldadura, sidebooms, control de calidad", "C\u00e9lulas de trabajo monitoreadas": "9 a 15 frentes simult\u00e1neos", "Automatizaci\u00f3n del llenado en terreno": "80% (mediante persistencia de equipos y maquinaria)"}}'::json, '["Automatizaci\u00f3n", "Transformaci\u00f3n Digital", "Miner\u00eda", "Control de Gesti\u00f3n", "Procesamiento de Datos", "Apps M\u00f3viles", "Operaciones", "Optimizaci\u00f3n de Procesos", "Eficiencia Operativa", "Gesti\u00f3n de Terreno."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('7615a33c-506c-441b-8ef7-87225a4a81ab', '00000000-0000-4000-8000-000000000000', 'Sistema de Integración Legacy y Automatización de Back-Office Hipotecario (RPA)', 'Robot de automatización de procesos robóticos (RPA) de nivel empresarial enfocado en la interoperabilidad de sistemas bancarios incomunicados para Scotiabank. El sistema orquesta la extracción masiva de casos desde bases de datos, descarga y procesa informes notariales complejos en formato PDF mediante técnicas avanzadas de depuración de datos no estructurados, y ejecuta la mantención automatizada de garantías en el sistema web legado (*Legacy*) del banco.',
    '### 📋 Contexto y Desafío Operacional
El departamento de Operaciones de Garantía Hipotecaria de Scotiabank gestiona diariamente las mantenciones y actualizaciones de los contratos de crédito. Este proceso requería que el equipo consultara manualmente una base de datos de casos pendientes, tomara el ID del documento e ingresara a una plataforma web interna moderna para descargar los informes legales emitidos por diversas notarías del país en formato PDF.

El proceso enfrentaba dos fricciones técnicas mayores:
1. **Complejidad y Variabilidad de los Documentos:** Los archivos PDF notariales carecían de una estructura estándar. Venían con formatos inconsistentes y datos "sucios", dificultando la localización exacta de los múltiples campos clave requeridos para la mantención.
2. **Incompatibilidad de Sistemas (Silos Tecnológicos):** Una vez extraída la información, los operadores debían transcribirla ingresando a un sistema web antiguo e institucional del banco. Esta plataforma legada no poseía comunicación ni APIs de integración con el portal moderno de descargas, generando un flujo de trabajo manual, repetitivo, lento y propenso a errores de digitación en datos financieros críticos.

### 🛠️ Solución Implementada (Acción)
Desarrollé e implementé un flujo automatizado de extremo a extremo utilizando la arquitectura estándar de la industria para resolver la brecha de integración entre sistemas:

* **Orquestación y Robustez (RPA):** Diseñé el robot bajo el framework empresarial **UiPath REFramework**, asegurando una ejecución controlada por estados, manejo seguro de excepciones de negocio y de sistema, y un historial completo de logs para auditoría interna.
* **Ingeniería de Datos en PDFs Inconsistentes:** Implementé lógica de parsing avanzada mediante código **.NET** y `UiPath` para leer y limpiar los strings de los PDFs "sucios". Utilicé métodos ingeniosos de extracción para normalizar los datos dispersos y asegurar que los campos críticos de la garantía hipotecaria se capturaran de forma exacta y estructurada en archivos temporales **JSON**.
* **Integración y Automatización de Navegación Web:** El robot automatiza la navegación asíncrona bi-plataforma a través del navegador Edge. Primero interactúa con el portal moderno para extraer el insumo, y posteriormente inyecta de forma precisa la información depurada en los campos correspondientes del sistema legado más antiguo, actuando como un puente de comunicación de datos en tiempo real.
* **Persistencia y Control de Versiones:** El proceso inicia consumiendo las colas de trabajo directamente desde consultas optimizadas en **SQL** y todo el ciclo de código fue versionado rigurosamente utilizando **Git**.', '["UiPath REFramework", ".NET (VB.NET/C#)", "SQL", "Microsoft Edge Automation", "PDF Data Extraction", "JSON", "Git", "Legacy Web Integration."]'::json, '2024-01-01', '', '', '{"Rendimiento & Negocio": {"Eficiencia Operativa": "Liberaci\u00f3n de tiempo cr\u00edtico en el Back-Office de Operaciones de Garant\u00eda", "Brecha de Integraci\u00f3n resuelta": "100% automatizada sin necesidad de desarrollo de APIs en sistemas antiguos", "Consistencia de la Informaci\u00f3n": "Validaci\u00f3n cross-system asegurando que la data del PDF calce exactamente con el registro del cliente", "Tasa de error en digitaci\u00f3n de garant\u00edas": "Reducida a 0% mediante inyecci\u00f3n directa de datos depurados"}, "Tecnolog\u00eda & Arquitectura": {"Framework Utilizado": "UiPath REFramework (State Machine)", "Origen de Transacciones": "Base de datos relacional orientada a SQL", "Motor de Lectura de Datos": "UiPath PDF Automation + L\u00f3gica de Expresiones en .NET", "Automatizaci\u00f3n de Interfaz": "UI Automation sobre Browser Microsoft Edge", "Formato de Intercambio Local": "Estructuras estructuradas en formato JSON"}, "Operaciones & Interoperabilidad": {"Sistemas Integrados": "2 plataformas web independientes (Portal Moderno y Sistema Legado)", "Manejo de Excepciones": "Clasificaci\u00f3n autom\u00e1tica de casos de dif\u00edcil lectura para revisi\u00f3n humana (Business Rule Exception)", "Tipo de Insumo Procesado": "Informes notariales en PDF no estructurados con alta variabilidad", "Trazabilidad del Proceso": "Control de cambios de estados en base de datos mediante ID de Documento"}}'::json, '["RPA", "Sistemas Legados", "Procesamiento de PDFs", "Operaciones Hipotecarias", "Integraci\u00f3n de Sistemas", "UiPath", "SQL", "Back-Office", "Banca", "Automatizaci\u00f3n Web."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('08781a71-4265-4bcb-9369-0a5a3216a244', '00000000-0000-4000-8000-000000000000', 'Pipeline ETL de Migración Cloud e Integración de Datos Financieros FactSet', '**Proyecto de Ingeniería de Datos y Migración Cloud** para BICE Inversiones enfocado en el diseño, desarrollo y optimización de pipelines ETL masivos. Automatiza la extracción, limpieza y estandarización de grandes volúmenes de datos financieros históricos y en tiempo real desde servidores locales (*On-Premise*) hacia Google Cloud Platform (GCP), integrando la suite analítica de FactSet mediante procedimientos almacenados optimizados y flujos corporativos en Talend.',
    '### 📋 Contexto y Desafío Operacional
BICE Inversiones requería modernizar su infraestructura analítica migrando su repositorio de datos financieros desde servidores locales (*On-Premise*) hacia un entorno moderno en la nube de Google Cloud Platform (GCP). El objetivo estratégico era centralizar la información transaccional e histórica del banco y enriquecerla mediante la integración de **FactSet**, una plataforma de provisión de datos financieros globales utilizada para el análisis de portafolios y gestión de patrimonios.

El desafío de ingeniería radicaba en la criticidad y el volumen de la información: los datos financieros venían segmentados en estructuras complejas y de difícil acceso. Era imperativo garantizar el cumplimiento de estrictos estándares de calidad del dato (*Data Quality*), latencia mínima, integridad referencial absoluta y seguridad bancaria durante todo el proceso de tránsito y transformación antes de disponibilizar la data en la nube para la toma de decisiones del área de inversiones.

### 🛠️ Solución Implementada (Acción)
Diseñé y ejecuté la arquitectura de integración y movimiento de datos utilizando herramientas y metodologías de nivel empresarial para entornos de alto rendimiento:

* **Ingeniería de Datos con SQL Avanzado:** Desarrollé y optimicé estructuras de bases de datos relacionales mediante **Stored Procedures** (Procedimientos Almacenados) complejos. Estos motores intermedios se encargaron de realizar la limpieza profunda, normalización y depuración de datos duplicados o inconsistentes directamente en el origen transaccional.
* **Construcción de Pipelines con Talend:** Programé flujos **ETL** (Extracción, Transformación y Carga) corporativos utilizando **Talend**. Diseñé la lógica de orquestación para la extracción asíncrona de los servidores locales, aplicando reglas de negocio financieras complejas y validaciones cruzadas que aseguraron la consistencia de los datos antes de su carga final.
* **Migración e Integración Multifuente (On-Premise to Cloud):** Implementé los canales de comunicación y carga de datos desde la infraestructura local hacia los almacenes analíticos de **Google Cloud**, integrando las estructuras de esquemas de **FactSet**. Esto facilitó la centralización de datos macroeconómicos, precios de activos y métricas operacionales de mercado en un solo ecosistema en la nube.
* **Gobernanza e Interoperabilidad:** Actué como nexo técnico para traducir los requerimientos del área de negocio y analistas financieros en estructuras de datos optimizadas, reduciendo los tiempos de ejecución de consultas pesadas y garantizando la trazabilidad del dato (*Data Lineage*).', '["Talend Open Studio (ETL)", "SQL", "Stored Procedures", "Google Cloud Platform (GCP)", "FactSet Financial Data", "On-Premise Servers", "Data Warehousing", "Data Quality", "Linux/Bash Scripting."]'::json, '2024-01-01', '', '', '{"Gobernanza & Calidad": {"Seguridad del Dato": "Tr\u00e1nsito cifrado desde infraestructura local hacia la nube", "Estrategia de Carga": "ETL / Pipeline de Datos Automatizado", "Normalizaci\u00f3n de Datos": "Estandarizaci\u00f3n de nomenclaturas financieras y tipos de activos", "Validaci\u00f3n de Integridad": "Automatizada en tr\u00e1nsito mediante reglas Talend"}, "Rendimiento & Negocio": {"Impacto Estrat\u00e9gico": "Disponibilizaci\u00f3n de datos optimizados para an\u00e1lisis de portafolios y toma de decisiones", "Interoperabilidad lograda": "Fusi\u00f3n exitosa de data hist\u00f3rica interna con feeds globales de FactSet", "Eficiencia de Procesamiento": "Reducci\u00f3n en tiempos de carga y procesamiento anal\u00edtico masivo", "Calidad del Dato (Data Quality Target)": "Garant\u00eda de consistencia absoluta entre origen y destino"}, "Tecnolog\u00eda & Infraestructura": {"Entorno de Origen": "Servidores Locales On-Premise (BICE Inversiones)", "Entorno de Destino": "Google Cloud Platform (GCP)", "L\u00f3gica de Base de Datos": "Stored Procedures (Procedimientos Almacenados) Optimizados", "Herramienta ETL Principal": "Talend Enterprise Data Integration", "Proveedor de Data Externa": "FactSet Insight & Data Feeds"}}'::json, '["Ingenier\u00eda de Datos", "Migraci\u00f3n Cloud", "ETL", "Talend", "SQL Avanzado", "Google Cloud", "FactSet", "Finanzas", "Big Data", "Inteligencia de Negocios."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('0785d731-f762-4a6d-8b70-b26a1267097b', '00000000-0000-4000-8000-000000000000', 'Plataforma Analítica y Módulo de Cobertura para la Mitigación de Riesgos Cambiarios (Data Science)', '**Sistema analítico e interactivo de Data Science** desarrollado para el Banco Internacional con el objetivo de cuantificar y mitigar los riesgos cambiarios en inversiones mediante instrumentos derivados. Diseñado en Python con procesamiento masivo en Pandas y modelamiento estadístico en SciPy, implementa una interfaz ejecutiva dinámica en Dash y Plotly para la evaluación de estrategias de cobertura financiera, hito técnico que consolidó la obtención del *EY Data Science Bronze Badge*.',
    '### 📋 Contexto y Desafío Operacional
En el sector bancario y de inversiones de alta exigencia, las fluctuaciones del mercado de divisas representan un riesgo crítico para los portafolios institucionales. El Banco Internacional requería robustecer sus capacidades analíticas para la gestión de riesgos cambiarios asociados a inversiones expuestas que utilizaban instrumentos financieros derivados[cite: 1, 2].

El desafío consistía en transformar flujos de variables macroeconómicas y datos transaccionales financieros dispersos en un modelo cuantitativo unificado. El área de gestión requería evaluar de forma inmediata el impacto de diferentes escenarios de mercado y modelar estrategias de cobertura (*hedging*) eficientes, lo cual exigía una herramienta interactiva que superara las limitaciones de los reportes estáticos y permitiera a los tomadores de decisiones visualizar riesgos complejos en tiempo real.

### 🛠️ Solución Implementada (Acción)
Diseñé y ejecuté el desarrollo de un módulo de ingeniería financiera y ciencia de datos de extremo a extremo, cumpliendo con los estándares globales de calidad analítica exigidos por la metodología de certificación corporativa de EY:

* **Ingeniería de Datos y Analítica Cuantitativa:** Utilicé **Python** y la biblioteca **Pandas** para la ingesta, limpieza profunda y manipulación de series de tiempo financieras complejas. Implementé modelos matemáticos y estadísticos utilizando **SciPy** para evaluar volatilidades, correlaciones de activos y efectividad de coberturas.
* **Desarrollo del Entorno Analítico Interactivo:** Construí un dashboard ejecutivo interactivo utilizando **Dash** y **Plotly**. Esta interfaz permite realizar simulaciones dinámicas de portafolios, visualizar distribuciones de riesgo y analizar la sensibilidad de los instrumentos derivados ante variaciones del tipo de cambio mediante gráficos de alta fidelidad.
* **Marcos de Arquitectura y Buenas Prácticas:** Estructuré el módulo bajo los pilares de la ciencia de datos aplicada a negocios, aislando de forma estricta la lógica de cálculo matemático del renderizado visual de la interfaz.

### 🥇 Certificación de Excelencia (EY Data Science Bronze Badge)
Este proyecto sirvió como la evidencia técnica fundamental para la adjudicación de la medalla internacional **EY Analytics - Data Science - Bronze**[cite: 1, 2]. Para su aprobación por el comité revisor global, completé un riguroso proceso de documentación académica (*Experience Evidence Form*), demostrando habilidades de:
* **Gobernanza y Confidencialidad:** Redacción bajo estrictos estándares éticos, aplicando técnicas de anonimización para omitir datos de identificación personal de clientes o miembros del banco.
* **Aplicación Práctica y Cambio de Comportamiento:** Validación de la capacidad de traducir conceptos estadísticos avanzados en soluciones de software de alto impacto operacional y financiero para el cliente.', '["Python", "Pandas", "SciPy", "Dash (Plotly)", "Plotly.js", "Git", "HTML5/CSS3 (Estructuras de layout anal\u00edtico)", "Jupyter Notebooks."]'::json, '2024-01-01', '', '', '{"Gobernanza & Credenciales": {"Certificaci\u00f3n Asociada": "EY Analytics - Data Science - Bronze Medal", "Est\u00e1ndar de Documentaci\u00f3n": "EEF (Experience Evidence Form) bajo normas APA", "Evaluaci\u00f3n de Comportamiento": "Pr\u00e1ctica y cambio de comportamiento validada en entorno real", "Pol\u00edticas de Datos Aplicadas": "Confidencialidad bancaria absoluta y anonimizaci\u00f3n de stakeholders"}, "Tecnolog\u00eda & Ciencia de Datos": {"Framework del Dashboard": "Dash (Plotly Framework)", "Lenguaje de Programaci\u00f3n": "Python", "Motor Gr\u00e1fico Interactivo": "Plotly.js", "Motor de Modelamiento Estad\u00edstico": "SciPy (Scientific Computing Tools)", "Librer\u00eda de Manipulaci\u00f3n de Datos": "Pandas"}, "Rendimiento & Impacto de Negocio": {"\u00c1rea de Aplicaci\u00f3n": "Gesti\u00f3n de Riesgo Cambiario y Estrategias de Cobertura (Hedging)", "Interactividad Lograda": "Transici\u00f3n de reportes est\u00e1ticos a simulaciones de escenarios en tiempo real", "Tipo de Activos Evaluados": "Inversiones institucionales e Instrumentos Derivados", "Impacto en la Toma de Decisiones": "Visualizaci\u00f3n intuitiva de m\u00e9tricas anal\u00edticas complejas para mesas de dinero"}}'::json, '["Data Science", "Gesti\u00f3n de Riesgos", "Instrumentos Derivados", "Finanzas Cuantitativas", "Dashboards Anal\u00edticos", "Python", "Banca", "Modelamiento Estad\u00edstico", "Cobertura Financiera."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('7b60ff2d-e646-4bfe-8a3f-e71cf7be92ac', '00000000-0000-4000-8000-000000000000', 'Sistema Event-Driven para Procesamiento e Ingesta de Pólizas de Seguros en Tiempo Real (RPA)', 'Robot de automatización e integración híbrida: que opera en modalidad continua (24/7) para la gestión y activación de pólizas en Scotiabank Corredora de Seguros. El sistema captura eventos por correo electrónico, extrae información no estructurada, consume APIs de validación empresarial mediante integraciones criptográficas en Python y actualiza en tiempo real los sistemas internos del banco (*Core Bancario*), notificando de forma automática al cliente el estado de su aprobación.',
    '### 📋 Contexto y Desafío Operacional
La Corredora de Seguros de Scotiabank requería procesar de manera inmediata las respuestas de aceptación o rechazo de seguros emitidas por los clientes. El flujo tradicional dependía de la revisión periódica de bandejas de entrada corporativas y la posterior digitación manual de los datos del cliente en múltiples plataformas internas para activar o dar de baja las pólizas.

Este enfoque presentaba tres problemas críticos: el retraso en la activación del seguro (dejando al cliente desprotegido durante horas), la alta carga administrativa de monitoreo constante y la complejidad técnica de interactuar con servicios web y APIs de validación que requerían el manejo seguro de llaves de autenticación e intercambio de estructuras complejas de datos (JSON).

### 🛠️ Solución Implementada (Acción)
Desarrollé un ecosistema de automatización híbrido que funciona de manera ininterrumpida, integrando flujos de interfaz con lógica de desarrollo de software avanzada:

* **Arquitectura Orientada a Eventos:** Implementé un robot basado en **UiPath REFramework** configurado para monitorear continuamente bandejas de correo en tiempo real. Al detectar un asunto específico de aceptación/rechazo, gatilla de forma síncrona el flujo transaccional.
* **Consumo de APIs e Integración con Python:** Diseñé la lógica de conexión con los microservicios de validación del banco. Para las APIs más complejas que exigían el manejo de tokens dinámicos y llaves de seguridad (*API Keys*), integré scripts de **Python** que actúan como pasarelas seguras de comunicación para procesar los payloads en formato **JSON**. Realicé pruebas y mapeo de estos servicios utilizando **Postman**.
* **Sincronización del Core Bancario (SQL Server):** El robot extrae los datos del correo, los normaliza en una base de datos de staging en SQL Server y, tras superar las validaciones de las APIs, orquesta la actualización simultánea de los datos del cliente en los sistemas legados e internos del banco.
* **Ciclo de Notificación Automatizado:** Desarrollé el flujo de salida que discrimina el resultado de las reglas de negocio: en caso de aprobación, genera y envía la póliza activa y el kit de bienvenida al cliente; en caso de rechazo, actualiza el estado de la campaña y envía el cierre formal del caso, manteniendo la trazabilidad con control de versiones en **Git**.', '["UiPath REFramework", "Python", "Servicios API REST", "Postman", "SQL Server", ".NET", "JSON", "Git", "Microsoft Outlook Automation."]'::json, '2024-01-01', '', '', '{"Rendimiento & Negocio": {"Mitigaci\u00f3n de Riesgo": "Eliminaci\u00f3n de p\u00f3lizas sin activar o procesadas fuera de plazo legal", "Trazabilidad de respuestas": "100% de los casos (Aprobados y Rechazados) registrados con logs auditarles", "Tiempo de respuesta/procesamiento": "Segundos por caso tras la llegada del correo", "Tasa de error en actualizaci\u00f3n de sistemas": "0% mediante transaccionalidad controlada en SQL/APIs"}, "Disponibilidad & Cobertura": {"Sistemas Actualizados": "Core Bancario Interno + Bases de datos de la Corredora de Seguros", "R\u00e9gimen de Operaci\u00f3n": "Continuo (24/7 / Always-on)", "Automatizaci\u00f3n de Ciclo Cerrado": "Desde la lectura del correo hasta la notificaci\u00f3n final al cliente", "Disparador del Proceso (Trigger)": "Detecci\u00f3n de eventos por correo electr\u00f3nico en tiempo real"}, "Tecnolog\u00eda & Integraci\u00f3n": {"Motor de Base de Datos": "Microsoft SQL Server", "Arquitectura del Sistema": "H\u00edbrida (UiPath REFramework + Motores de Scripting Python)", "Seguridad de Credenciales": "Manejo seguro de API Keys y criptograf\u00eda mediante Python", "Protocolo de Comunicaci\u00f3n": "APIs RESTful (Payloads JSON)", "Herramienta de Testing de APIs": "Postman"}}'::json, '["RPA", "APIs", "Python", "Integraci\u00f3n de Sistemas", "Core Bancario", "Seguros", "Automatizaci\u00f3n 24/7", "SQL Server", "Event-Driven", "Transformaci\u00f3n Digital."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('18e1206e-2feb-4d90-a457-dd8ef9ae3635', '00000000-0000-4000-8000-000000000000', 'Procesamiento Automatizado de Telemarketing y Conciliación Back-Office (RPA)', 'Robot de automatización empresarial (RPA): desarrollado bajo arquitectura corporativa que centraliza, depura y valida transaccionalmente las ventas diarias de Telemarketing para Scotiabank. Procesa archivos masivos mediante reglas de negocio complejas en SQL, generando salidas estructuradas en formatos específicos (.TXT) listas para su inyección directa en plataformas externas de procesamiento financiero (Nexus), reduciendo a cero el procesamiento manual diario.',
    '### 📋 Contexto y Desafío Operacional
En el área de operaciones y Back-Office de Scotiabank, el canal de Telemarketing genera un volumen masivo de ventas diarias distribuidas en múltiples fuentes de información. Al cierre de cada jornada laboral, se requería recopilar de forma manual 6 archivos Excel críticos alojados en distintas carpetas compartidas de la red corporativa.

El desafío principal radicaba en la criticidad y el procesamiento de estos datos: la información venía cruda y requería una profunda depuración y validación respecto a complejas reglas de negocio internas del banco antes de poder ser autorizada. El proceso manual no solo consumía valiosas horas de la célula de operaciones del Back-Office, sino que incrementaba el riesgo operativo de fuga de datos o errores de digitación en la estructura de los archivos de salida, los cuales debían cumplir con un estándar sumamente estricto y específico en formato de texto plano (.TXT) para poder ser cargados en la plataforma de procesamiento financiero **Nexus**.

### 🛠️ Solución Implementada (Acción)
Diseñé y desarrollé un proceso de automatización integral de extremo a extremo utilizando herramientas de nivel empresarial para centralizar y asegurar la consistencia del flujo operativo:

* **Arquitectura de Software (RPA):** Implementé el robot utilizando **UiPath REFramework (Robotic Enterprise Framework)**, asegurando una solución escalable, con un manejo avanzado de excepciones (sistémicas y de negocio), persistencia de estados y logging detallado para auditoría.
* **Ingeniería y Procesamiento de Datos:** El robot automatiza la extracción asíncrona de los 6 archivos Excel desde las redes compartidas. Diseñé un motor intermedio en **SQL** para la ingesta y depuración de la data cruda, aplicando procedimientos de validación lógica basados en las reglas de negocio bancarias mediante código **.NET**.
* **Estandarización y Salida Estructurada:** El sistema automatizado procesa y clasifica las ventas del día dividiéndolas en dos tablas maestras de bases de datos. Finalmente, genera de manera automatizada archivos `.TXT` con la estructura de caracteres y posiciones requerida de manera exacta por **Nexus**, acompañados de un reporte detallado de casos rechazados con sus respectivos códigos de error para el análisis del equipo de operaciones.
* **Control de Versiones:** Todo el ciclo de desarrollo, pruebas y despliegue del bot fue gestionado utilizando **Git**, garantizando buenas prácticas de ingeniería de software.', '["UiPath REFramework", "SQL", ".NET (VB.NET/C#)", "Git", "Microsoft Excel Automation", "Windows Credential Manager", "Nexus API/File Specifications."]'::json, '2024-01-01', '', '', '{"Operaciones & Volumen": {"Destino de la data": "Plataforma transaccional Nexus", "Or\u00edgenes de datos": "2 servidores / carpetas compartidas corporativas", "Frecuencia de ejecuci\u00f3n": "Diaria (Cierre de jornada de Telemarketing)", "Archivos procesados por ciclo": "6 archivos Excel consolidados"}, "Rendimiento & Calidad": {"Consistencia de datos": "Validaci\u00f3n masiva cruzada mediante motor de base de datos", "Trazabilidad de rechazos": "100% (Reporte automatizado de excepciones con c\u00f3digo de negocio)", "Tiempo de procesamiento manual": "Reducido a cero (0) en Back-Office", "Tasa de error en formato de salida (.TXT)": "0% (Garant\u00eda de cumplimiento estricto de especificaci\u00f3n Nexus)"}, "Tecnolog\u00eda & Arquitectura": {"Motor de Validaci\u00f3n": "SQL Queries & .NET Integration", "Manejo de Excepciones": "Autom\u00e1tico (System Exception vs Business Rule Exception)", "Gesti\u00f3n de Configuraci\u00f3n": "Assets de Orquestador / Git", "Framework de Automatizaci\u00f3n": "UiPath REFramework (State Machine)"}}'::json, '["RPA", "Automatizaci\u00f3n de Procesos", "Banca", "Back-Office", "Finanzas", "UiPath", "SQL", "Ingenier\u00eda de Datos", "Integraci\u00f3n de Sistemas", "Mitigaci\u00f3n de Riesgo Operativo."]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('b77dc2b7-37a5-4aae-ab7c-5172ed2566fa', '00000000-0000-4000-8000-000000000000', 'OppyTec - Business Management System', '**Plataforma inteligente de gestión integral para restaurantes y negocios gastronómicos** que combina control de inventario en tiempo real, recetas con costing automatizado, compras, facturación con IA, y reportes ejecutivos con insights predictivos — todo en una interfaz moderna, multi-tema y lista para usar.',
    'OppyTec no es un ERP genérico más. Es un **sistema vertical diseñado específicamente para la industria food service** que resuelve los problemas reales del día a día de restaurantes, cafeterías, hoteles, bares, pastelerías y servicios de catering.

Nuestra plataforma unifica en un solo lugar lo que antes requería múltiples herramientas: control de stock con trazabilidad completa por lote y vencimiento, gestión de recetas con cálculo automático de costos y márgenes, órdenes de compra inteligentes, facturación potenciada por inteligencia artificial (Google Gemini), y un panel ejecutivo con ingeniería de menú (matriz BCG), punto de equilibrio, prime cost, rotación de inventario y detección de anomalías en pérdidas.

Construida con tecnologías modernas (FastAPI + React 19 + PostgreSQL), es rápida, escalable, multi-tenant por schema, y completamente dockerizada para deployment inmediato.

### Highlights del Proyecto

- **🚀 Control de Stock en Tiempo Real** — Trazabilidad completa de cada movimiento con undo/redo, soporte multi-lote con fechas de vencimiento, transferencias entre bodegas, y snapshot de stock calculado con Polars para alto rendimiento
- **🤖 Facturación con Inteligencia Artificial** — Sube una foto de tu factura y Gemini extrae automáticamente proveedor, RUT, montos, impuestos, items y hasta detecta el país de origen. Genera audit flags y alertas de inconsistencias
- **📊 Ingeniería de Menú (BCG Matrix)** — Clasifica automáticamente tus platos en Estrellas, Perros, Vacas e Interrogantes según margen y popularidad. Toma decisiones de menú basadas en datos, no en corazonadas
- **📈 Reportes Ejecutivos con Insights IA** — No solo mostramos números: la IA analiza tu inventario, ventas y mermas para generar recomendaciones prescriptivas: fugas de dinero, sobrestock, oportunidades de ahorro
- **🛒 Flujo Completo de Compras** — Desde la orden al proveedor hasta la recepción con control de incidencias, notificaciones automáticas por email, fill rate, variación de precios y calendario de pagos
- **📐 Ingeniería de Costos** — Costo de receta calculado automáticamente, prime cost, punto de equilibrio, variación de precios de insumos. Saber exactamente cuánto cuesta cada plato
- **🧠 Proyecciones Inteligentes** — Forecasting de inventario basado en consumo histórico + eventos agendados. Anticipa desabastecimientos antes de que ocurran
- **🔔 Alertas Proactivas** — Stock crítico, productos próximos a vencer, anomalías en mermas (desviación estándar), productos cerca del punto de reorden. El sistema te avisa antes de que sea un problema
- **🏢 Multi-tenant Nativo** — Cada restaurante opera en su propio schema de PostgreSQL. Datos aislados, seguros y escalables
- **🎨 3 Temas Visuales Premium** — Light, Dark y Cosmic Blue (tema oscuro con animaciones nebula, destellos y glassmorphism). Una experiencia visual que encanta a los usuarios
- **📱 Mobile-First** — Interfaz responsive con drawer en móvil, selectores táctiles, escáner de códigos de barras y QR integrado
- **🔌 Integraciones Listas** — Exportación contable a SII (Chile), QuickBooks, Xero, Odoo, ContaPlus. Webhooks para integración con cualquier sistema externo. Google OAuth para login sin password
- **🔐 Seguridad Empresarial** — JWT dual (access + refresh tokens), cookies HttpOnly, roles granulares (propietario, admin, supervisor, usuario), permisos específicos por funcionalidad, historial de sesiones
- **🐳 Dockerizado** — docker-compose con PostgreSQL, Redis, pgAdmin y la API. Se levanta en segundos
- **🇨🇱 Hecho en Chile** — Soporte nativo para SII (libro de compras y ventas), moneda CLP, RUT, huso horario Santiago. Pero preparado para operar internacionalmente', '["Python 3.12", "FastAPI", "SQLAlchemy 2.0", "PostgreSQL 15", "Redis", "Alembic", "Google Gemini", "Authlib", "SQLAdmin", "Polars", "Sentry", "Docker", "React 19", "TypeScript 6", "Vite 8", "Tailwind CSS 3", "shadcn/ui (Radix)", "Axios", "TanStack React Query", "Framer Motion", "Recharts", "React Hook Form", "Zod", "Sonner", "Lucide React", "date-fns", "xlsx", "html5-qrcode", "Docker Compose", "AWS S3", "Resend API", "SMTP", "WebSockets", "Webhooks"]'::json, '2024-01-01', 'https://github.com/OppyTec/OppyTec_Backend', '', '{"Negocio": {"Ideal para": "Restaurantes, cafeter\u00edas, hoteles, bares, pasteler\u00edas, catering, casinos", "Pa\u00edses objetivo": "Chile (nativo) + Internacional", "Tipo de proyecto": "ERP vertical para food service", "Reducci\u00f3n estimada de mermas": "15-30% con tracking y alertas", "Tiempo estimado de implementaci\u00f3n": "Horas (SaaS), D\u00edas (on-premise)", "Ahorro estimado en costos operativos": "10-20% con ingenier\u00eda de men\u00fa y compras inteligentes"}, "Cobertura": {"Endpoints API": 140, "Componentes UI": 48, "P\u00e1ginas frontend": 20, "Reportes ejecutivos": 5, "M\u00f3dulos funcionales": 15, "Tablas en base de datos": 40, "Formatos de exportaci\u00f3n": 10}, "Seguridad": {"OAuth": "Google (web + mobile)", "Roles": 4, "Monitoreo": "Sentry (errores + tracing)", "Transmisi\u00f3n": "Cookies HttpOnly, HTTPS enforced", "Rate limiting": "Redis (configurable)", "Autenticaci\u00f3n": "JWT dual (access + refresh)", "Permisos granulares": 4}, "Rendimiento": {"Cache Redis TTL": "30 minutos", "Snapshot de stock": "Tiempo real (Polars)", "Latencia WebSocket": "< 50ms", "Pool de conexiones DB": "40 conexiones + 20 overflow", "Tiempo de respuesta API": "< 200ms (p95)", "Procesamiento de factura con IA": "5-15 segundos"}, "Tecnolog\u00eda": {"IA": "Google Gemini", "Cache": "Redis", "Frontend": "React 19 + TypeScript 5.x + Vite 6.x", "Contenedores": "Docker + Docker Compose", "Base de datos": "PostgreSQL 15", "Framework API": "FastAPI (async)", "Gestor Paquetes": "pnpm", "Lenguaje Backend": "Python 3.12"}, "Escalabilidad": {"Migraciones": "Alembic autom\u00e1ticas", "Arquitectura": "Multi-tenant por schema PostgreSQL", "Horizontal scaling": "Stateless, multiple instances", "Tiempo de deployment": "< 5 minutos (Docker)"}, "Disponibilidad": {"Backup": "PostgreSQL + snapshots", "Entornos": "Desarrollo, Test, Producci\u00f3n", "Uptime target": "99.9%", "Recuperaci\u00f3n ante fallos": "Autom\u00e1tica (Docker healthchecks + restart)"}}'::json, '["ERP", "Gesti\u00f3n de Inventario", "Restaurantes", "Food Service", "Hoteler\u00eda", "Gastronom\u00eda", "Control de Stock", "Facturaci\u00f3n Electr\u00f3nica", "IA Generativa", "Gemini", "FastAPI", "React", "Gesti\u00f3n de Recetas", "Ingenier\u00eda de Men\u00fa", "Food Cost", "Supply Chain", "Log\u00edstica", "Compras", "Reportes Ejecutivos", "Finanzas", "SII Chile", "Multi-tenant", "SaaS"]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('516e33d2-cf6c-4e3f-974f-e15555b47b69', '00000000-0000-4000-8000-000000000000', 'FastAlert - Sistema de Seguridad Vecinal con IoT y WhatsApp', 'Sistema de alerta vecinal que integra una cámara ESP32-CAM con notificaciones en tiempo real vía WhatsApp para la seguridad del vecindario.',
    'FastAlert es una plataforma de seguridad comunitaria que combina hardware IoT (ESP32-CAM), una API backend en Python/FastAPI, y una aplicación móvil en Flet para crear un sistema de alerta vecinal automatizado.

### Highlights del Proyecto

- **Activación multicanal**: Los vecinos pueden activar la alerta desde la app móvil Flet o mediante comandos de texto por WhatsApp (palabras clave: ALERTA, SOS, 🚨).
- **Captura de evidencia en vivo**: Al activarse la alerta, el ESP32-CAM captura una ráfaga de **5 fotos** en tiempo real y las envía automáticamente al grupo de WhatsApp vecinal.
- **Sirena local integrada**: El ESP32 activa un buzzer (sirena) en el lugar del evento como disuasivo físico.
- **Notificaciones vía WhatsApp**: Utiliza Evolution API como gateway de WhatsApp para enviar mensajes de texto e imágenes al grupo de vecinos de forma asíncrona.
- **Webhook bidireccional**: Recibe comandos desde WhatsApp para activar/detener la alarma, permitiendo interacción sin necesidad de la app.
- **Auto-apagado de seguridad**: La alarma se desactiva automáticamente tras **45 segundos** para evitar que quede activa indefinidamente si el ESP32 se desconecta.
- **Control de acceso por número telefónico**: Solo vecinos registrados con números autorizados pueden activar el sistema.
- **Polling eficiente del ESP32**: El microcontrolador consulta el estado de la alarma cada **1.5 segundos** con un consumo mínimo de recursos.
- **Cooldown anti-disparos múltiples**: Previene activaciones repetidas mientras la alarma ya está en curso.
- **Registro de eventos en base de datos**: Cada alerta queda registrada con timestamp, vecino responsable y cantidad de fotos capturadas.
- **Despliegue containerizado**: Todo el sistema (API + Evolution API + PostgreSQL) se despliega con Docker Compose.
- **App móvil multiplataforma**: Desarrollada en Flet (Python), compatible con Android, iOS y escritorio desde un solo código base.', '["Python", "FastAPI", "SQLAlchemy", "SQLite", "Pydantic", "Uvicorn", "Flet", "HTTPX", "Arduino/ESP32-CAM", "Evolution API (WhatsApp Gateway)", "Docker", "Docker Compose", "PostgreSQL"]'::json, '2024-01-01', 'https://github.com/jcampillay8/FastAlert', '', '{"Polling ESP32": "1.5s", "R\u00e1faga de fotos por evento": "5", "Tiempo m\u00e1ximo de alerta activa": "45s", "Tasa de \u00e9xito en env\u00edo de fotos": ">95%", "Latencia de notificaci\u00f3n WhatsApp": "<3s", "Tiempo de respuesta ESP32 -> Backend": "<1.5s"}'::json, '["Seguridad", "IoT", "AppMobile", "ESP32", "WhatsApp", "Vecinal", "Alarma", "Python"]'::json, '', true);


INSERT INTO oppy.proyectos 
    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, fecha_proyecto, link_github, link_demo, kpis, tags, youtube_url, is_active)
    VALUES ('23f5fd30-f9c1-4e73-bbc7-1f058391d42f', '00000000-0000-4000-8000-000000000000', 'OppyTalent (Portafolio Inteligente)', 'Plataforma interactiva construida con un backend asíncrono en FastAPI (Python) y base de datos PostgreSQL, integrada con agentes de IA autónomos con persistencia de memoria para interactuar y responder consultas ejecutivas y métricas de trayectoria profesional en tiempo real. Despliegue automatizado contenerizado en Railway acoplado a la capa de seguridad, optimización y administración DNS global de Cloudflare.',
    'Plataforma interactiva construida con un backend asíncrono en FastAPI (Python) y base de datos PostgreSQL, integrada con agentes de IA autónomos con persistencia de memoria para interactuar y responder consultas ejecutivas y métricas de trayectoria profesional en tiempo real. Despliegue automatizado contenerizado en Railway acoplado a la capa de seguridad, optimización y administración DNS global de Cloudflare.', '["FastAPI", "Python", "PostgreSQL", "IA", "Docker", "Railway", "Cloudflare"]'::json, '2024-01-01', '', '', '{"Comuna": "Illapel", "Entidad": "Gobierno Regional de Coquimbo.", "Proyecto": "FNDR", "Inversi\u00f3n": "$599.323.000", "Superficie": "286.5 m2.", "Ubicaci\u00f3n": "Localidad de Huintil Sur.", "A\u00f1o de aprobaci\u00f3n": "2019"}'::json, '["FastAPI", "Python", "PostgreSQL", "IA", "Docker", "Railway", "Cloudflare"]'::json, '', true);

COMMIT;

-- ==============================================================
-- 3. DEMO CHAT SCRIPTS TABLE & SEED
-- ==============================================================
CREATE TABLE IF NOT EXISTS oppy.demo_chat_scripts (
    usuario_id UUID PRIMARY KEY REFERENCES oppy.usuarios(id) ON DELETE CASCADE,
    step_1 TEXT NOT NULL,
    step_2 TEXT NOT NULL,
    step_3 TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL
);

INSERT INTO oppy.demo_chat_scripts (usuario_id, step_1, step_2, step_3, is_active)
SELECT 
    u.id, 
    '👋 ¡Hola! Soy el clon digital de prueba de un(a) **' || COALESCE(p.ocupacion, 'Profesional') || '**. Mi objetivo es mostrarte cómo OppyTalent puede extraer tu experiencia, certificaciones y habilidades directamente de tu currículum para representarte profesionalmente las 24 horas del día ante reclutadores o clientes. ¿Qué te parece?',
    '🤖 Normalmente, si yo fuera un usuario real, estaría analizando tus preguntas mediante Inteligencia Artificial y respondiendo de forma estratégica basándome **estrictamente en los datos de mi portafolio** (mi experiencia, proyectos, KPIs, etc.). Por motivos de seguridad y para evitar un mal uso en esta vitrina pública, en este perfil de prueba solo respondo con estos mensajes automáticos... ¡pero imagina el potencial que esta tecnología tiene para potenciar tu propia carrera!',
    '🔒 **Límite de demostración alcanzado.**\n\nSi quieres ver el verdadero poder de la IA conversacional trabajando a tu favor respondiendo preguntas reales, te invito a crear tu propia cuenta. Puedes cargar tu CV, personalizar tu diseño y probar tu Clon Digital en vivo.\n\n¡Es gratis y solo toma un par de minutos!\n\n¿Deseas ir al registro? [SÍ](/register) / [NO](#)',
    true
FROM oppy.usuarios u 
JOIN oppy.perfiles p ON u.id = p.usuario_id 
WHERE u.email LIKE '%@demo.oppytalent.com'
ON CONFLICT (usuario_id) DO UPDATE SET
    step_1 = EXCLUDED.step_1,
    step_2 = EXCLUDED.step_2,
    step_3 = EXCLUDED.step_3,
    is_active = EXCLUDED.is_active;

