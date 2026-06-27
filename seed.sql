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
COMMIT;

-- ==============================================================
-- 3. DEMO CHAT SCRIPTS TABLE & SEED
-- ==============================================================
CREATE TABLE IF NOT EXISTS oppy.demo_chat_scripts (
    usuario_id UUID PRIMARY KEY REFERENCES oppy.usuarios(id) ON DELETE CASCADE,
    step_1 TEXT NOT NULL,
    step_2 TEXT NOT NULL,
    step_3 TEXT NOT NULL
);

INSERT INTO oppy.demo_chat_scripts (usuario_id, step_1, step_2, step_3)
SELECT 
    u.id, 
    '👋 ¡Hola! Soy el clon digital de prueba de un(a) **' || COALESCE(p.ocupacion, 'Profesional') || '**. Mi objetivo es mostrarte cómo OppyTalent puede extraer tu experiencia, certificaciones y habilidades directamente de tu currículum para representarte profesionalmente las 24 horas del día ante reclutadores o clientes. ¿Qué te parece?',
    '🤖 Normalmente, si yo fuera un usuario real, estaría analizando tus preguntas mediante Inteligencia Artificial y respondiendo de forma estratégica basándome **estrictamente en los datos de mi portafolio** (mi experiencia, proyectos, KPIs, etc.). Por motivos de seguridad y para evitar un mal uso en esta vitrina pública, en este perfil de prueba solo respondo con estos mensajes automáticos... ¡pero imagina el potencial que esta tecnología tiene para potenciar tu propia carrera!',
    '🔒 **Límite de demostración alcanzado.**\n\nSi quieres ver el verdadero poder de la IA conversacional trabajando a tu favor respondiendo preguntas reales, te invito a crear tu propia cuenta. Puedes cargar tu CV, personalizar tu diseño y probar tu Clon Digital en vivo.\n\n¡Es gratis y solo toma un par de minutos!\n\n¿Deseas ir al registro? [SÍ](/register) / [NO](#)'
FROM oppy.usuarios u 
JOIN oppy.perfiles p ON u.id = p.usuario_id 
WHERE u.email LIKE '%@demo.oppytalent.com'
ON CONFLICT (usuario_id) DO UPDATE SET
    step_1 = EXCLUDED.step_1,
    step_2 = EXCLUDED.step_2,
    step_3 = EXCLUDED.step_3;

